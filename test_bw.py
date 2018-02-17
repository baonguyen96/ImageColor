# driver program for linear scaling and histogram equalization (BW only)

import cv2
import sys
import color
import bw
import shutil
import os


if not os.path.exists("images"):
    os.mkdir("images")

name_input = 'images/bw.png'
name_output_he = 'bw_he_1199.png'
name_output_ls = 'bw_ls_1199.png'
w1 = 0.1
h1 = 0.1
w2 = 0.9
h2 = 0.9

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
new_img_ls = color.linear_scaling(W1, H1, W2, H2, input_image)
cv2.imshow("Linear Scaling", new_img_ls)
cv2.imwrite(name_output_ls, new_img_ls)
shutil.move("./" + name_output_ls, "./images/" + name_output_ls)

# histogram equalization
# new_img_he = color.histogram_equalization(W1, H1, W2, H2, input_image_copy)
# cv2.imshow("Histogram Equalization", new_img_he)    # why does not show?
# cv2.imwrite(name_output_he, new_img_he)
# shutil.move("./" + name_output_he, "./images/" + name_output_he)

# wait for key to exit
cv2.waitKey(0)
cv2.destroyAllWindows()
