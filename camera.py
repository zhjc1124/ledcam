import cv2
height = 480
width = 640
d = 45.5 * 2/640


def mirrored(gray):
    mirror = gray.copy()
    for i in xrange(height):
        for j in xrange(width):
            mirror[i, width - 1 - j] = gray[i, j]
    return mirror

cap = cv2.VideoCapture(0)
for i in xrange(20):
    _, img = cap.read()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = mirrored(gray)
cv2.imwrite("gray.jpg", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()