import cv2
import time
import pycurl
from pathlib import Path

def upload(filename,station,unixtime,size,setno):
    c = pycurl.Curl()
    uploadUrl = 'localhost:3030/upload'
    url =  uploadUrl + '?station={}&unixtime={}&size={}&setno={}'.format(station,unixtime,size,setno)
    c.setopt(c.URL, url )


    c.setopt(c.HTTPPOST, [
        ('files', (c.FORM_FILE, filename))
    ])
    c.perform()
    c.close()

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
        jpgFileName = Path(filename).stem + '.jpg'
        cv2.imwrite(jpgFileName, img_bmp, [int(cv2.IMWRITE_JPEG_QUALITY), 20])
        jpgFiles.append(jpgFileName)
    return jpgFiles

def resize_to_m(bmpFiles):
    jpgFiles =[]
    for filename in bmpFiles:
        img_bmp = cv2.imread(filename,1)
        jpgFileName = Path(filename).stem + '.jpg'
        cv2.imwrite(jpgFileName, img_bmp, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
        jpgFiles.append(jpgFileName)
    return jpgFiles

def resize_to_l(bmpFiles):
    jpgFiles =[]
    for filename in bmpFiles:
        img_bmp = cv2.imread(filename,1)
        jpgFileName = Path(filename).stem + '.jpg'
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
    



bmpSelected =  ['./test/innertube.bmp','./test/innertube1.bmp','./test/innertube2.bmp']
station='innertube'
unixtime=1565553447  
setno='77888555' 
    

resize_and_upload(bmpSelected,station,unixtime,setno)