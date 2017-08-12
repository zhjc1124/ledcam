
# -*- coding:utf-8 -*-

import cv2
import numpy as np
from locate import locate_ as lc

import socket
import time
import os

if socket.gethostname() == "raspberrypi":
    from lcd import display
else:
    def display(x):
        print x
cam = 0
points = ((0, 20), (0, 0), (0, -20))

height = 480
width = 640
d = 46.5 * 2/640


def calculate(leds, leds_):
    # print leds, leds_

    def cal(led, led_):
        delta_y = (led[0] - height/2) * d
        delta_x = (led[1] - width/2) * d
        x = led_[0] - delta_x
        y = led_[1] + delta_y
        return x, y
    x, y = np.mean([cal(led, led_) for led, led_ in zip(leds, leds_)], axis=0)
    if x < -32:
        x+= -4
    # elif x < -26:
    #     x += -2
    elif x < -6:
        x += -1
    return x, y


def mirrored(gray):
    mirror = gray.copy()
    for i in xrange(height):  # 元素循环
        for j in xrange(width):
            mirror[i, width - 1 - j] = gray[i, j]
    return mirror


def main():

    times = 0
    while True:
        times += 1
        print "time:%s" % times
        try:
            time.sleep(2)
            os.popen('fswebcam  -r 640x480 --no-banner --no-timestamp ./img.jpg -F 10')
            img = cv2.imread("img.jpg")
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = mirrored(gray)
            cv2.imwrite("gray.jpg", gray)

            leds = lc(gray)

            if len(leds):
                if len(leds) == 1:
                    led = leds[0]
                    if led[0] > height/2.0:
                        leds_ = points[:1]
                    else:
                        leds_ = points[2:]

                if len(leds) == 2:
                    if sum([led[0]for led in leds]) > height:
                        leds_ = points[:2]
                    else:
                        leds_ = points[1:]
                if len(leds) == 3:
                    leds_ = points[::]

                print leds_
                x, y = calculate(leds, leds_)
                info = 'x:%.1f,y:%.1f\n' % (x, y)
                if x > 0:
                    info += 'Right'
                else:
                    info += ' Left'
                if y > 0:
                    info += '    Up'
                else:
                    info += ', Down'
                display(info)
                print 'display success'

        except Exception:
            pass


if __name__ == '__main__':
    main()



