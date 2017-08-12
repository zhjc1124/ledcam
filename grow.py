# -*- coding:utf-8 -*-

import cv2
import numpy as np

height = 480
width = 640

gray = cv2.imread('gray.jpg', 0)
check = set({})
points = set({})

for x in xrange(height):
    for y in xrange(width):
        points.add((x, y))

classed = []
while True:
    if not check:
        if not points:
            break
        x, y = points.pop()
        if gray[x][y] > 240:
            check.add((x, y))
            classed.append(set([]))
    else:
        x, y = check.pop()
        classed[-1].add((x, y))
        print classed
        neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for m, n in neighbors:
            try:
                print 'distance:', abs(int(gray[x][y]) - int(gray[x + m][y + n])), (x, y), (x+m, y+n)
                if (x + m, y + n) in classed[-1]:
                    pass
                elif abs(int(gray[x][y]) - int(gray[x + m][y + n])) < 20:
                    classed[-1].add((x + m, y + n))
                    if (x + m, y + n) in points:
                        points.discard((x+m, y+n))
                        check.add((x+m, y+n))
            except IndexError:
                pass
leds = map(lambda k: np.mean(k, axis=0), classed)
print len(classed), map(len, classed), leds