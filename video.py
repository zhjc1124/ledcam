# -*- coding:utf-8 -*-

import cv2
import numpy as np
# 去掉废的10张python ~/ledcam/position.py & > ~/log.txt

cap = cv2.VideoCapture(0)
height = 480
width = 640
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)

cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)

for i in xrange(10):
    ret, frame = cap.read()

d = 0.0875


def draw_line(img, lines):
    result = img.copy()
    # for x in xrange(height):
    #     for y in xrange(width):
    #         result[x][y] = 0

    for line in lines:
        rho = line[0]  # 第一个元素是距离rho
        theta = line[1]  # 第二个元素是角度theta
        if (theta < (np.pi / 4.)) or (theta > (3. * np.pi / 4.0)):  # 垂直直线
            # 该直线与第一行的交点
            pt1 = (int(rho / np.cos(theta)), 0)
            # 该直线与最后一行的交点
            pt2 = (int((rho - result.shape[0] * np.sin(theta)) / np.cos(theta)), result.shape[0])
            # 绘制一条白线
            cv2.line(result, pt1, pt2, 255)
        else:  # 水平直线
            # 该直线与第一列的交点
            pt1 = (0, int(rho / np.sin(theta)))
            # 该直线与最后一列的交点
            pt2 = (result.shape[1], int((rho - result.shape[1] * np.cos(theta)) / np.sin(theta)))
            # 绘制一条直线
            cv2.line(result, pt1, pt2, 255, 1)
    # cv2.imshow('Img', img)
    cv2.imshow('Result', result)


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
    # lines = cv2.HougheLines(edges, 1, np.pi / 180, 118)  # 这里对最后一个参数使用了经验型的值
    # lines = lines[0]
    # print lines

    # print gray[gray == 255]
    # cv2.imshow("gray", gray)
    draw_line(gray, [[height/2, np.pi/2], [width/2, 0]])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("gray.jpg", gray)
        break
# cv2.imwrite("img.jpg", img)

cv2.destroyAllWindows()
cap.release()
