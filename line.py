# coding=utf-8
import cv2
import numpy as np

height = 480
width = 640


def linesort(img):
    img = cv2.GaussianBlur(img, (3, 3), 0)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 118)  # 这里对最后一个参数使用了经验型的值
    try:
        lines = lines[0]
    except TypeError:
        return []
    sorted_lines = [lines[0]]
    for line in lines:
        for i in xrange(len(sorted_lines)):
            print line, sorted_lines[i], abs(line[0] - sorted_lines[i][0]) <30, abs(line[1] - sorted_lines[i][1])<0.02
            if abs(line[0] - sorted_lines[i][0]) < 30 and abs(line[1] - sorted_lines[i][1]) < 0.02:
                sorted_lines[i] = [(line[0] + sorted_lines[i][0])/2, (line[1] + sorted_lines[i][1])/2]
                break
        else:
            sorted_lines.append(line)
    return sorted_lines


def draw_line(img, lines):
    result = img.copy()
    for x in xrange(height):
        for y in xrange(width):
            result[x][y] = 0

    for line in lines:
        rho = line[0]  # 第一个元素是距离rho
        theta = line[1]  # 第二个元素是角度theta
        print rho
        print theta
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
    cv2.imshow('Img', img)
    cv2.imshow('Result', result)

if __name__ == "__main__":
    img = cv2.imread("gray.jpg", 0)
    lines = linesort(img)
    draw_line(img, lines)
    cv2.waitKey(0)
    cv2.destroyAllWindows()