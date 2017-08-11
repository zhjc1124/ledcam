# -*- coding:utf-8 -*-

import cv2
import numpy as np

height = 480
width = 640


def locate(gray):
    def check_point(x_, y_, value):
        neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for m, n in neighbors:
            try:
                # print 'distance:', abs(int(gray[x_][y_]) - int(gray[x_ + m][y_ + n])), (x_, y_), (x_+m, y_+n), value
                if flag[x_ + m][y_ + n]:
                    pass
                elif abs(int(gray[x_][y_]) - int(gray[x_ + m][y_ + n])) < 20:
                    flag[x_ + m][y_ + n] = value
                    classed[int(value) - 1].append([x_ + m, y_ + n])
                    check_point(x_ + m, y_ + n, value)
            except IndexError:
                pass
    classed = []
    flag = np.zeros([height, width], dtype=np.int)
    for x in xrange(height):
        for y in xrange(width):
            if flag[x][y] == 0:
                if gray[x][y] > 240:
                    classed.append([])
                    classed[-1].append([x, y])
                    check_point(x, y, len(classed))
            else:
                check_point(x, y, flag[x][y])

    for i in xrange(len(classed)):
        if len(classed[i]) < 30:
            classed.pop(i)
            continue
    leds = map(lambda k: np.mean(k, axis=0), classed)
    print len(classed), map(len, classed), leds
    return leds

if __name__ == "__main__":
    gray = cv2.imread('gray.jpg', 0)
    locate(gray)


