
# -*- coding:utf-8 -*-

import cv2
import numpy as np
from locate import locate
from line import line_sort, draw_line
import socket

if socket.gethostname() == 'raspberrypi':
    from lcd import display
else:
    def display(x):
        print x

points = ((0, 15), (-20, -20), (20, -20))

height = 480
width = 640
d = 0.0875


def calculate(leds, leds_):
    def cal(led, led_):
        delta_y = (led[0] - 240) * d
        delta_x = (led[1] - 320) * d
        x = led_[0] - delta_x
        y = led_[1] + delta_y
        return x, y
    x, y = np.mean([cal(led, led_) for led, led_ in zip(leds, leds_)], axis=0)
    return x, y


def mirrored(gray):
    mirror = gray.copy()
    for i in xrange(height):  # 元素循环
        for j in xrange(width):
            mirror[i, width - 1 - j] = gray[i, j]
    return mirror


# while True:
gray = cv2.imread("gray.jpg", 0)
# cap = cv2.VideoCapture(0)
# cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 960)
# for i in xrange(10):
#     ret, frame = cap.read()
# _, img = cap.read()
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gray = mirrored(gray)
vertical, horizontal = line_sort(gray)
leds = locate(gray)
print vertical, horizontal, leds
if len(leds):
    if len(leds) == 1:
        if vertical:
            if vertical[1] < 320:
                leds_ = points[1:2]
            else:
                leds_ = points[2:]
        else:
            leds_ = points[0:1]

    if len(leds) == 2:
        if vertical:
            if vertical[1] < 320:
                leds_ = points[:2]
            else:
                leds_ = points[0]
    if len(leds) == 3:
        leds_ = points[::]
    x, y = calculate(leds, leds_)
display('x: %s\ny: %s' % (x, y))

cv2.imshow("gray", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()




