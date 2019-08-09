import cv2
import time

img = cv2.imread('./test/rattler.png',0)
mask = cv2.imread('./mask/rattler.png',0)
res = cv2.bitwise_and(img,img,mask = mask)

cv2.imshow('innertube',res)
cv2.waitKey(0)
cv2.destroyAllWindows()