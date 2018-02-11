import cv2
import numpy as np
import sys
import bw
import color
import os

name_input = 'images/bw.png'
name_output = 'bw7788.png'
w1 = 0.7
h1 = 0.7
w2 = 0.8
h2 = 0.8

inputImage = cv2.imread(name_input, cv2.IMREAD_COLOR)
if inputImage is None:
    print(sys.argv[0], ": Failed to read image from: ", name_input)
    sys.exit()

cv2.imshow("Input", inputImage)

rows, cols, bands = inputImage.shape  # bands == 3
W1 = round(w1 * (cols - 1))
H1 = round(h1 * (rows - 1))
W2 = round(w2 * (cols - 1))
H2 = round(h2 * (rows - 1))

# print('rows = {}, cols = {}, bands = {}'.format(rows, cols, bands))
# print('w1 = {}, h1 = {}, w2 = {}, h2 = {}'.format(w1, h1, w2, h2))
# print('W1 = {}, H1 = {}, W2 = {}, H2 = {}'.format(W1, H1, W2, H2))

new_img = bw.linear_scaling(W1, H1, W2, H2, inputImage)
cv2.imshow("New", new_img)
cv2.imwrite(name_output, new_img)

# move the images to the images folder
os.rename("./" + name_output, "./images/" + name_output)

# wait for key to exit
cv2.waitKey(0)
cv2.destroyAllWindows()
