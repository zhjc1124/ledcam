import cv2
height = 480
width = 640
d = 45.5 * 2/640
import os


def mirrored(gray):
    mirror = gray.copy()
    for i in xrange(height):
        for j in xrange(width):
            mirror[i, width - 1 - j] = gray[i, j]
    return mirror


os.popen('fswebcam -d /dev/video0 -r 640x480 --no-banner --no-timestamp ./img.jpg > ./info')
img = cv2.imread("img.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = mirrored(gray)

cv2.imwrite("gray.jpg", gray)
cv2.imshow('gray', gray)
for x in xrange(height):
    for y in xrange(width):
        if gray[x][y] > 230:
            gray[x][y] = 255
        else:
            gray[x][y] = 0

cv2.imshow('test', gray)

cv2.waitKey(0)
cv2.destroyAllWindows()