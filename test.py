"""
Bao Nguyen
BCN140030
CS 4391.001
"""

import os
import shutil
from collections import Counter
import cv2
import numpy as np
import color


def test_dict_1():
    index = "0.3"
    dictionary = ['0.1', '0.1', '0.2']
    dictionary += [str.format('%.1f' % 0.3)]
    # dictionary[3] = 3
    c = Counter(dictionary)
    c[index] = 3
    print(dict)
    print(c['0.1'])
    print(c)


def test_dict_2():
    dictionary = ['0.4', '0.1', '0.1', '0.2', '0.3', '0.3', '0.3']
    c = Counter(dictionary)
    print(c)
    print(c['0.4'])
    print(c[0.4])
    print()

    c_copy = c.copy()
    c_copy['0.4'] = 5
    print(c_copy)
    print(c)
    print()

    for key, elem in c.items():
        print('{}, {}'.format(key, elem))
    print()

    c = sorted(c)
    print(c)


def test_power():
    print(2 ** (1/1.5))


def test_matrix():
    matrix = np.matrix('1 1 1')
    print(matrix)
    print(matrix.item(0))


def test_image_transform():
    if not os.path.exists("old_images"):
        os.mkdir("old_images")
    org_bgr_img = cv2.imread("old_images/lenna.bmp")
    cv2.imshow("Original BGR", org_bgr_img)
    non_linear_bgr_img = org_bgr_img * 1/255
    xyz_img = color.bgr2xyz(non_linear_bgr_img)     # non_linear_rgb -> linear_rgb -> xyz
    luv_img = color.xyz2luv(xyz_img)
    new_xyz_img = color.luv2xyz(luv_img)
    new_non_linear_bgr_img = color.xyz2bgr(new_xyz_img)     # xyz -> linear_rgb -> non_linear_rgb
    # new_linear_bgr_img = color.xyz2bgr(xyz_img)
    new_bgr_img = np.floor((new_non_linear_bgr_img * 255))
    cv2.imwrite("new_fruits.png", new_bgr_img)
    shutil.move("./new_fruits.png", "./old_images/new_fruits.png")
    cv2.imshow("Transform back BGR", new_bgr_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test_histogram_equalization_hi_values():
    org_bgr_img = cv2.imread("old_images/lenna.bmp")
    w1 = 0.6
    h1 = 0.3
    w2 = 0.8
    h2 = 0.7
    rows, cols, bands = org_bgr_img.shape

    W1 = round(w1 * (cols - 1))
    H1 = round(h1 * (rows - 1))
    W2 = round(w2 * (cols - 1))
    H2 = round(h2 * (rows - 1))
    color.histogram_equalization(W1, H1, W2, H2, org_bgr_img)


def test_histogram_equalization_opencv():
    img = cv2.imread('old_images/bw.png', 0)
    cv2.imshow("Input", img)
    res = cv2.equalizeHist(img)
    cv2.imshow("Output", res)
    cv2.imwrite('bw_he_opencv.png', res)
    shutil.move("./bw_he_opencv.png", "./old_images/bw_he_opencv.png")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


test_histogram_equalization_opencv()
