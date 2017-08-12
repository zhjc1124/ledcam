import cv2
import numpy as np


img_zo = cv2.resize(gray, (480, 640), interpolation=cv2.INTER_AREA)
cv2.imshow('zoom', img_zo)