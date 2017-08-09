# -*- coding:utf-8 -*-

import cv2
import numpy as np
# 去掉废的10张
cap = cv2.VideoCapture(1)
for i in range(10):
    ret, frame = cap.read()

while True:
    ret, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Image", img)
    cv2.imshow("gray", gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# cv2.imwrite("img.jpg", img)
# cv2.imwrite("gray.jpg", gray)


cv2.destroyAllWindows()
cap.release()
