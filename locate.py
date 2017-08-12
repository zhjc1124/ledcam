# -*- coding:utf-8 -*-

import cv2
import numpy as np
from line import line_sort
import sys
sys.setrecursionlimit(3500)

height = 480
width = 640


def locate(gray, show=True):
    def check_point(x_, y_, value):
        neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for m, n in neighbors:
            try:
                # print (x_, y_), (x_ + m, y_ + n), gray[x_][y_], gray[x_ + m][y + n]
                if flag[x_ + m][y_ + n]:
                    pass
                elif abs(int(gray[x_][y_]) - int(gray[x_ + m][y_ + n])) < 10 and gray[x_ + m][y_ + n] > 220:
                    flag[x_ + m][y_ + n] = value
                    classed[int(value) - 1].append((x_ + m, y_ + n))
                    check_point(x_ + m, y_ + n, value)
            except IndexError:
                pass
    classed = []
    horizontal = line_sort(gray)
    if len(horizontal):
        rho = horizontal[0]
        theta = horizontal[1]
        pt1 = (int(rho / np.sin(theta)), 0)
        # 该直线与最后一列的交点
        pt2 = (int((rho - width * np.cos(theta)) / np.sin(theta)), width)
        h_border = min(pt1[0], pt2[0])
        if h_border > height/2:
            for x in xrange(h_border, height):
                for y in xrange(width):
                    gray[x][y] = 0

    flag = np.zeros([height, width], dtype=np.int)
    for x in xrange(height):
        for y in xrange(width):
            if flag[x][y] == 0:
                if gray[x][y] > 230:
                    classed.append([])
                    classed[-1].append((x, y))
                    check_point(x, y, len(classed))
            else:
                check_point(x, y, flag[x][y])
    print len(classed), [len(i) for i in classed]
    classed = [i for i in classed if len(i) > 20 and min(np.array(i).var(axis=0)) < 100]
    if not classed:
        return []

    leds = map(lambda k: np.average(k, axis=0, weights=[[gray[x][y]]*2 for x, y in k]), classed)
    if leds and show:
        result = np.zeros([height, width])
        for led in classed:
            for point in led:
                x, y = point[0], point[1]
                result[x][y] = 255
        cv2.imshow("result", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return leds

if __name__ == "__main__":
    gray = cv2.imread('gray.jpg', 0)
    print locate(gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()