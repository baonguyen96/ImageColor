"""
Bao Nguyen
BCN140030
CS 4391.001
"""

# driver program for linear scaling and histogram equalization

import cv2
import sys
import color
import shutil
import os
import time


if not os.path.exists("images"):
    os.mkdir("images")

name_input = 'images/fruits.jpg'
name_output_he = 'fruits_he_4455__.png'
name_output_ls = 'fruits_ls_4455__.png'
w1 = 0.4
h1 = 0.4
w2 = 0.5
h2 = 0.5

input_image = cv2.imread(name_input, cv2.IMREAD_COLOR)          # for linear scaling
input_image_copy = cv2.imread(name_input, cv2.IMREAD_COLOR)     # for histogram equalization

if input_image is None:
    print(sys.argv[0], ": Failed to read image from: ", name_input)
    sys.exit()

cv2.imshow("Input", input_image)

rows, cols, bands = input_image.shape  # bands == 3

W1 = round(w1 * (cols - 1))
H1 = round(h1 * (rows - 1))
W2 = round(w2 * (cols - 1))
H2 = round(h2 * (rows - 1))

# linear scaling
ls_start = time.time()
new_img_ls = color.linear_scaling(W1, H1, W2, H2, input_image)
cv2.imwrite(name_output_ls, new_img_ls)
new_img_ls = cv2.imread(name_output_ls, cv2.IMREAD_COLOR)
cv2.imshow("Linear Scaling", new_img_ls)
ls_end = time.time()

# histogram equalization
he_start = time.time()
new_img_he = color.histogram_equalization(W1, H1, W2, H2, input_image_copy)
cv2.imwrite(name_output_he, new_img_he)
new_img_he = cv2.imread(name_output_he, cv2.IMREAD_COLOR)
cv2.imshow("Histogram Equalization", new_img_he)
he_end = time.time()

# move new images to the images directory
shutil.move("./" + name_output_ls, "./images/" + name_output_ls)
shutil.move("./" + name_output_he, "./images/" + name_output_he)

print('Linear scaling:         {} seconds'.format(ls_end - ls_start))
print('Histogram equalization: {} seconds'.format(he_end - he_start))

# wait for key to exit
print('Press any key to continue...')
cv2.waitKey(0)
cv2.destroyAllWindows()
