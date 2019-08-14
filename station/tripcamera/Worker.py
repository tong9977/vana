import cv2
import time
import pycurl
from pathlib import Path
from glob import glob
import numpy as np
import os

class Worker:
    def  __init__(self, station,srcpath,uploadUrl):
        self.station = station
        self.srcpath = srcpath
        self.uploadUrl= uploadUrl

    def __uploadFiles(self,filenames,station,unixtime,setno,size):
        c = pycurl.Curl()
 
        url =  self.uploadUrl + '?station={}&unixtime={}&size={}&setno={}'.format(station,unixtime,size,setno)
        c.setopt(c.URL, url )
    
        targetfiles =[]
        for filename in filenames:
            targetfiles.append(('files', (c.FORM_FILE, filename)))
    
        c.setopt(c.HTTPPOST,targetfiles)
        c.perform()
        c.close()
    
    
    def __resize_to_s(self,bmpFiles):
        jpgFiles =[]
        for filename in bmpFiles:
            img_bmp = cv2.imread(filename,1)
            jpgFileName = self.srcpath +Path(filename).stem + '.jpg'
            cv2.imwrite(jpgFileName, img_bmp, [int(cv2.IMWRITE_JPEG_QUALITY), 20])
            jpgFiles.append(jpgFileName)
        return jpgFiles
    
    def __resize_to_m(self,bmpFiles):
        jpgFiles =[]
        for filename in bmpFiles:
            img_bmp = cv2.imread(filename,1)
            jpgFileName = self.srcpath+Path(filename).stem + '.jpg'
            cv2.imwrite(jpgFileName, img_bmp, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
            jpgFiles.append(jpgFileName)
        return jpgFiles
    
    def __resize_to_l(self,bmpFiles):
        jpgFiles =[]
        for filename in bmpFiles:
            img_bmp = cv2.imread(filename,1)
            jpgFileName = self.srcpath+Path(filename).stem + '.jpg'
            cv2.imwrite(jpgFileName, img_bmp, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            jpgFiles.append(jpgFileName)
        return jpgFiles
    
    def __resize_and_upload(self,bmpFiles,station,unixtime,setno):
        jpgFiles = self.__resize_to_s(bmpFiles)
        self.__uploadFiles(jpgFiles,station,unixtime,setno,size='s')
        
        jpgFiles = self.__resize_to_m(bmpFiles)
        self.__uploadFiles(jpgFiles,station,unixtime,setno,size='m')
        
        jpgFiles = self.__resize_to_l(bmpFiles)
        self.__uploadFiles(jpgFiles,station,unixtime,setno,size='l')
    
    def __get_first_set(self):
    
        bmpfiles = sorted(glob('{}*.bmp'.format(self.srcpath)))
        if len(bmpfiles) > 0 :
        
            unixtime,setno,count = Path(bmpfiles[0]).stem.split("-", 2)
            bmps = sorted(glob('{}*{}*.bmp'.format(self.srcpath,setno)))
            
            photos = []
            for bmp in bmps :
                u,s,c = Path(bmp).stem.split("-", 2)
                o = {'filepath': bmp, 'unixtime': u, 'setno': s, 'count': int(c)}
                photos.append(o)
    
            return photos
    
        else :
            return []
        
    
    def __print_list(self,photos):
        for p in photos:
            print('{} | {} | {} | {}'.format(p.get("unixtime"),p.get("setno"),p.get("count"),p.get("filepath")))
    
    def __pick(self,photos,number):
        count_max = max(photos, key=lambda x:x['count']).get('count')
        print(count_max)
    
        count_max_idx = 0 
        for i in range(0,len(photos)):
            if photos[i].get('count') != count_max:
                count_max_idx = count_max_idx+1
            else:
                break
    
        print(count_max_idx)        
        selected = []
        
        start=count_max_idx-number+1
        if start <= 0:
            start = 0

        end = count_max_idx+1

        for i in range(start, end):
            selected.append(photos[i])
        return selected        
    
    def exec(self):
        photos = self.__get_first_set();
        if len(photos) > 0:
            self.__print_list(photos)
            print('--------')
            selected_photos = self.__pick(photos,4)
            self.__print_list(selected_photos)
    
            station=self.station
            unixtime=int(selected_photos[0].get('unixtime')[0:10])
            setno=selected_photos[0].get('setno')
    
            bmpSelected = []
            for p in selected_photos:
                bmpSelected.append(p.get('filepath'))
    
            self.__resize_and_upload(bmpSelected,station,unixtime,setno)
        
            #clean
            filestoclean = sorted(glob('{}*{}*.*'.format(self.srcpath,setno)))
            for file in filestoclean:
                os.remove(file)
    
