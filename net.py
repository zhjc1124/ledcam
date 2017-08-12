import cv2
gray = cv2.imread('gray.jpg', 0)
circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 100, param1=100, param2=10, minRadius=0, maxRadius=10)
print circles
# cv2.imshow("img", gray)
# cv2.waitKey(0)