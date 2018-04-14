"""
Bao Nguyen
BCN140030
CS 4391.001
"""

import os
import sys
import cv2
import color


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

inputImage = cv2.imread(name_input, cv2.IMREAD_COLOR)
if inputImage is None:
    print(sys.argv[0], ": Failed to read image from: ", name_input)
    sys.exit()

# create the images directory if not already exists
if not os.path.exists("images"):
    os.mkdir("images")

cv2.imshow("Input image", inputImage)

rows, cols, bands = inputImage.shape  # bands == 3
W1 = round(w1 * (cols - 1))
H1 = round(h1 * (rows - 1))
W2 = round(w2 * (cols - 1))
H2 = round(h2 * (rows - 1))

new_img = color.histogram_equalization(W1, H1, W2, H2, inputImage)
cv2.imwrite(name_output, new_img)
new_img = cv2.imread(name_output, cv2.IMREAD_COLOR)
cv2.imshow("Histogram Equalization", new_img)

# move the old_images to the old_images folder
os.rename("./" + name_output, "./images/" + name_output)

# wait for key to exit
print('Press any key to continue...')
cv2.waitKey(0)
cv2.destroyAllWindows()
