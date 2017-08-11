# -*- coding:utf-8 -*-

import cv2
import numpy as np
# 去掉废的10张
cap = cv2.VideoCapture(1)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 960)
for i in xrange(10):
    ret, frame = cap.read()

height = 480
width = 640
d = 0.0875


def mirrored(gray):
    mirror = gray.copy()
    for i in xrange(height):  # 元素循环
        for j in xrange(width):
            mirror[i, width - 1 - j] = gray[i, j]
    return mirror
while True:
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = mirrored(gray)

    # img = cv2.GaussianBlur(gray, (3, 3), 0)
    # edges = cv2.Canny(img, 50, 150, apertureSize=3)
    # lines = cv2.HoughLines(edges, 1, np.pi / 180, 118)  # 这里对最后一个参数使用了经验型的值
    # lines = lines[0]
    # print lines

    # print gray[gray == 255]
    cv2.imshow("gray", gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# cv2.imwrite("img.jpg", img)
cv2.imwrite("gray.jpg", gray)


cv2.destroyAllWindows()
cap.release()
