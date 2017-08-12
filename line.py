# coding=utf-8
import cv2
import numpy as np

height = 480
width = 640


def line_sort(img):
    img = cv2.GaussianBlur(img, (3, 3), 0)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 118)  # 这里对最后一个参数使用了经验型的值
    # return lines[0]
    # if lines is not None:
    #     vertical = [line for line in lines[0] if -np.pi / 8.0 <= line[1] <= np.pi / 8.0]
    #
    #     if len(vertical):
    #         vertical = [line for line in vertical if line[1] == min(vertical, key=lambda i: abs(i[1]))[1]]
    #         if np.mean(vertical, axis=0)[0] > 240:
    #             fun = min
    #         else:
    #             fun = max
    #         vertical = fun(vertical, key=lambda i: i[0])
    #     horizontal = [line for line in lines[0] if 3 * np.pi / 8.0 <= line[1] <= 5 * np.pi / 8.0]
    #     if len(horizontal):
    #         horizontal = [line for line in horizontal if line[1] == min(horizontal, key=lambda i: abs(i[1] - np.pi / 2))[1]]
    #         if np.mean(horizontal, axis=0)[0] > 320:
    #             fun = min
    #         else:
    #             fun = max
    #             horizontal = fun(horizontal, key=lambda i: i[0])
    #
    #     if show:
    #         if len(vertical) or len(horizontal):
    #             draw_line(img, (vertical, horizontal))
    #     return vertical, horizontal
    #
    # else:
    #
    #     return [], []
    if lines is not None:
        horizontal = [line for line in lines[0] if 3 * np.pi / 8.0 <= line[1] <= 5 * np.pi / 8.0]
        if len(horizontal):
            horizontal = [line for line in horizontal if line[1] == min(horizontal, key=lambda i: abs(i[1] - np.pi / 2))[1]]
            horizontal = min(horizontal, key=lambda i: i[0])
            return horizontal
    return []


def draw_line(img, lines):
    result = img.copy()
    for x in xrange(height):
        for y in xrange(width):
            result[x][y] = 0
    print lines
    for line in lines:
        if len(line):
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
    cv2.imshow('line', result)

if __name__ == "__main__":
    img = cv2.imread("gray.jpg", 0)
    lines = line_sort(img)
    print lines
    # draw_line(img, lines)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
