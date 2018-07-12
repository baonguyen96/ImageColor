"""
Bao Nguyen
BCN140030
CS 4391.001
"""

import cv2
import sys
import color
import shutil
import os
import time


if not os.path.exists("old_images"):
    os.mkdir("old_images")

if len(sys.argv) != 7:
    print(sys.argv[0], ": takes 6 arguments. Not ", len(sys.argv) - 1)
    print("Expecting arguments: w1 h1 w2 h2 ImageIn ImageOut.")
    print("Example:", sys.argv[0], " 0.2 0.1 0.8 0.5 fruits.jpg out.png")
    sys.exit()

w1 = float(sys.argv[1])
h1 = float(sys.argv[2])
w2 = float(sys.argv[3])
h2 = float(sys.argv[4])
name_input = sys.argv[5]
name_output = sys.argv[6]

if w1 < 0 or h1 < 0 or w2 <= w1 or h2 <= h1 or w2 > 1 or h2 > 1:
    print(" arguments must satisfy 0 <= w1 < w2 <= 1, 0 <= h1 < h2 <= 1")
    sys.exit()

path, file = os.path.split(name_output)
name_output_he = 'he_' + file
name_output_ls = 'ls' + file

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

# move new old_images to the old_images directory
shutil.move("./" + name_output_ls, "./images/" + name_output_ls)
shutil.move("./" + name_output_he, "./images/" + name_output_he)

# print('Linear scaling:         {} seconds'.format(ls_end - ls_start))
# print('Histogram equalization: {} seconds'.format(he_end - he_start))

# wait for key to exit
print('Press any key to continue...')
cv2.waitKey(0)
cv2.destroyAllWindows()
