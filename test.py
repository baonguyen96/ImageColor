from collections import Counter
import color
import numpy as np
import cv2
import os
import shutil
import time


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
    new_i = []
    l = 7.9999999
    l_as_str = str.format("%.6f" % l)
    new_i += ['7.999999']
    # new_i['7.999999'] = 3
    print(new_i)
    print(Counter(new_i))


def test_power():
    print(2 ** (1/1.5))


def test_matrix():
    matrix = np.matrix('1 1 1')
    print(matrix)
    print(matrix.item(0))


def test_image_transform():
    if not os.path.exists("images"):
        os.mkdir("images")
    org_bgr_img = cv2.imread("images/lenna.bmp")
    cv2.imshow("Original BGR", org_bgr_img)
    non_linear_bgr_img = org_bgr_img * 1/255
    xyz_img = color.bgr2xyz(non_linear_bgr_img)     # non_linear_rgb -> linear_rgb -> xyz
    luv_img = color.xyz2luv(xyz_img)
    new_xyz_img = color.luv2xyz(luv_img)
    new_non_linear_bgr_img = color.xyz2bgr(new_xyz_img)     # xyz -> linear_rgb -> non_linear_rgb
    # new_linear_bgr_img = color.xyz2bgr(xyz_img)
    new_bgr_img = np.floor((new_non_linear_bgr_img * 255))
    cv2.imwrite("new_fruits.png", new_bgr_img)
    shutil.move("./new_fruits.png", "./images/new_fruits.png")
    cv2.imshow("Transform back BGR", new_bgr_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


test_image_transform()
