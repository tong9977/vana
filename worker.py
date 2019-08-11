import cv2
import time
import pycurl

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

def uploadFiles(filenames,station,unixtime,size,setno):
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

img_bmp = cv2.imread('./test/innertube.bmp',1)
cv2.imwrite('img_100.jpg', img_bmp, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
cv2.imwrite('img_60.jpg', img_bmp, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
cv2.imwrite('img_20.jpg', img_bmp, [int(cv2.IMWRITE_JPEG_QUALITY), 20])

uploadFiles(['img_100.jpg','img_60.jpg','img_20.jpg'],station='innertube',unixtime=1565553447,size='s',setno='77888555')



