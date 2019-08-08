import PyCapture2
import cv2
import numpy as np
import time
import shutil

def bb_intersection_over_union(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])
 
	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
 
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
 
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = interArea / float(boxAArea + boxBArea - interArea)
 
	# return the intersection over union value
	return iou


def print_build_info():
    lib_ver = PyCapture2.getLibraryVersion()
    print('PyCapture2 library version: %d %d %d %d' % (lib_ver[0], lib_ver[1], lib_ver[2], lib_ver[3]))
    print()

def print_camera_info(cam):
    cam_info = cam.getCameraInfo()
    print('\n*** CAMERA INFORMATION ***\n')
    print('Serial number - %d' % cam_info.serialNumber)
    print('Camera model - %s' % cam_info.modelName)
    print('Camera vendor - %s' % cam_info.vendorName)
    print('Sensor - %s' % cam_info.sensorInfo)
    print('Resolution - %s' % cam_info.sensorResolution)
    print('Firmware version - %s' % cam_info.firmwareVersion)
    print('Firmware build time - %s' % cam_info.firmwareBuildTime)
    print()

def enable_embedded_timestamp(cam, enable_timestamp):
    embedded_info = cam.getEmbeddedImageInfo()
    if embedded_info.available.timestamp:
        cam.setEmbeddedImageInfo(timestamp = enable_timestamp)
        if enable_timestamp :
            print('\nTimeStamp is enabled.\n')
        else:
            print('\nTimeStamp is disabled.\n')


def grab(cam):

    cam.startCapture()
    image = cam.retrieveBuffer()
    cam.stopCapture()
    timestamp = image.getTimeStamp()


    image.save('tmp.bmp'.encode('utf-8'),PyCapture2.IMAGE_FILE_FORMAT.BMP)
    img = cv2.imread('tmp.bmp',0)
  
    return img,timestamp,image


def grab_images(cam, num_images_to_grab):
    prev_ts = None
    for i in range(num_images_to_grab):
        try:
            image = cam.retrieveBuffer()
        except PyCapture2.Fc2error as fc2Err:
            print('Error retrieving buffer : %s' % fc2Err)
            continue

        ts = image.getTimeStamp()
        if prev_ts:
            diff = (ts.cycleSeconds - prev_ts.cycleSeconds) * 8000 + (ts.cycleCount - prev_ts.cycleCount)
            print('Timestamp [ %d %d ] - %d' % (ts.cycleSeconds, ts.cycleCount, diff))
        prev_ts = ts


    #newimg = image.convert(PyCapture2.PIXEL_FORMAT.BGR)
    #print('Saving the last image to fc2TestImage.png')
    #newimg.save('now.png'.encode('utf-8'), PyCapture2.IMAGE_FILE_FORMAT.PNG)
#
# Example Main
#

# Print PyCapture2 Library Information
print_build_info()

# Ensure sufficient cameras are found
bus = PyCapture2.BusManager()
num_cams = bus.getNumOfCameras()
print('Number of cameras detected: ', num_cams)
if not num_cams:
    print('Insufficient number of cameras. Exiting...')
    exit()

# Select camera on 0th index
c = PyCapture2.Camera()
uid = bus.getCameraFromIndex(0)
c.connect(uid)
print_camera_info(c)

# Enable camera embedded timestamp
enable_embedded_timestamp(c, True)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

print('Starting image capture...')
fgbg = cv2.createBackgroundSubtractorMOG2()

while 1:
    #grab_images(c, 1)
    img,ts,orgImage = grab(c)

    
    fgmask = fgbg.apply(img)
    count = cv2.countNonZero(fgmask)
 
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,'Timestamp [ {:04d} {:04d} {}]'.format(ts.cycleSeconds, ts.cycleCount,count),(20,20), font, .5,(255,255,255),1,cv2.LINE_AA)
    #cv2.imshow('innertube',img)
    #cv2.imshow('fgmask',fgmask)
    
    if count>=80000 :
        filename ='{:04d}-{:04d}.png '.format(ts.cycleSeconds, ts.cycleCount)
    
        newimg = orgImage.convert(PyCapture2.PIXEL_FORMAT.BGR)
        print('Saving {}'.format(filename))
        newimg.save('tmp.png'.encode('utf-8'), PyCapture2.IMAGE_FILE_FORMAT.PNG)
        newPath = shutil.copy('tmp.png', './test/{}'.format(filename))

    
    print(count)

    #cv2.imwrite('{:04d}-{:04d}.png '.format(ts.cycleSeconds, ts.cycleCount),fgmask)
    #time.sleep(1)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    

# Disable camera embedded timestamp
enable_embedded_timestamp(c, True)
c.disconnect()

#input('Done! Press Enter to exit...\n')