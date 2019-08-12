import cv2
import time
import pycurl
from pathlib import Path
from glob import glob
import numpy as np
import os

srcPath = '/vanaramdisk/'

def uploadFiles(filenames,station,unixtime,setno,size):
    c = pycurl.Curl()
    uploadUrl = 'localhost:3030/upload'
    url =  uploadUrl + '?station={}&unixtime={}&size={}&setno={}'.format(station,unixtime,size,setno)
    c.setopt(c.URL, url )

    targetfiles =[]
    for filename in filenames:
        targetfiles.append(('files', (c.FORM_FILE, filename)))

    c.setopt(c.HTTPPOST,targetfiles)
    c.perform()
    c.close()


def resize_to_s(bmpFiles):
    jpgFiles =[]
    for filename in bmpFiles:
        img_bmp = cv2.imread(filename,1)
        jpgFileName = srcPath+Path(filename).stem + '.jpg'
        cv2.imwrite(jpgFileName, img_bmp, [int(cv2.IMWRITE_JPEG_QUALITY), 20])
        jpgFiles.append(jpgFileName)
    return jpgFiles

def resize_to_m(bmpFiles):
    jpgFiles =[]
    for filename in bmpFiles:
        img_bmp = cv2.imread(filename,1)
        jpgFileName = srcPath+Path(filename).stem + '.jpg'
        cv2.imwrite(jpgFileName, img_bmp, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
        jpgFiles.append(jpgFileName)
    return jpgFiles

def resize_to_l(bmpFiles):
    jpgFiles =[]
    for filename in bmpFiles:
        img_bmp = cv2.imread(filename,1)
        jpgFileName = srcPath+Path(filename).stem + '.jpg'
        cv2.imwrite(jpgFileName, img_bmp, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        jpgFiles.append(jpgFileName)
    return jpgFiles

def resize_and_upload(bmpFiles,station,unixtime,setno):
    jpgFiles = resize_to_s(bmpFiles)
    uploadFiles(jpgFiles,station,unixtime,setno,size='s')
    
    jpgFiles = resize_to_m(bmpFiles)
    uploadFiles(jpgFiles,station,unixtime,setno,size='m')
    
    jpgFiles = resize_to_l(bmpFiles)
    uploadFiles(jpgFiles,station,unixtime,setno,size='l')

def get_first_set():

    bmpfiles = sorted(glob('{}*.bmp'.format(srcPath)))
    if len(bmpfiles) > 0 :
    
        unixtime,setno,count = Path(bmpfiles[0]).stem.split("-", 2)
        bmps = sorted(glob('{}*{}*.bmp'.format(srcPath,setno)))
        
        photos = []
        for bmp in bmps :
            u,s,c = Path(bmp).stem.split("-", 2)
            o = {'filepath': bmp, 'unixtime': u, 'setno': s, 'count': int(c)}
            photos.append(o)

        return photos

    else :
        return []
    

def print_list(photos):
    for p in photos:
        print('{} | {} | {} | {}'.format(p.get("unixtime"),p.get("setno"),p.get("count"),p.get("filepath")))

def pick(photos,number):
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
    for i in range(count_max_idx-number+1, count_max_idx+1):
        selected.append(photos[i])
    return selected        

def exec():
    photos = get_first_set();
    if len(photos) > 0:
        print_list(photos)
        print('--------')
        selected_photos = pick(photos,4)
        print_list(selected_photos)

        station='rattler'
        unixtime=int(selected_photos[0].get('unixtime')[0:10])
        setno=selected_photos[0].get('setno')

        bmpSelected = []
        for p in selected_photos:
            bmpSelected.append(p.get('filepath'))

        resize_and_upload(bmpSelected,station,unixtime,setno)
    
        #clean
        filestoclean = sorted(glob('{}*{}*.*'.format(srcPath,setno)))
        for file in filestoclean:
            os.remove(file)

    
exec()

