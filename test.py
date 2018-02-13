# test using histogram equalization from opencv

import cv2
import numpy as np


img = cv2.imread('images/bw.png', 0)
equ = cv2.equalizeHist(img)
cv2.imwrite('images/bw_he_opencv.png', equ)
