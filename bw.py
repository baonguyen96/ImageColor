# can only process bw images

import cv2
import numpy as np
import math

# not include a column for i (array index itself already)
H_I = 0
F_I = NEW_I = 1
F_I_CALC = 2
FLOOR_F_I_CALC = 3


def ls_transform(x, a, b, A, B):
    tmp = (x - a) * (B - A)
    tmp = tmp / (b - a)
    return tmp + A


def linear_scaling(x1, y1, x2, y2, org_img):
    lookup_table = np.zeros((256, 2), dtype=int)
    new_img = org_img
    min_i = 257
    max_i = -1

    h, w, bands = org_img.shape
    print("linear scaling")
    print('x1 = {}, y1 = {}, x2 = {}, y2 = {}'.format(x1, y1, x2, y2))
    print('image size = {}x{}'.format(w, h))

    # count histogram
    for x in range(x1, x2):
        for y in range(y1, y2):
            b, g, r = new_img[y, x]
            lookup_table[g][H_I] += 1   # count frequency

            if g < min_i:
                min_i = g
            elif g > max_i:
                max_i = g

    print('max i = {}, min i = {}'.format(max_i, min_i))

    # build a lookup table
    for i in range(256):
        if min_i <= i <= max_i:
            lookup_table[i][NEW_I] = ls_transform(i, min_i, max_i, 0, 255)
        elif i < min_i:
            lookup_table[i][NEW_I] = 0
        else:
            lookup_table[i][NEW_I] = 255

    for x in range(x1, x2):
        for y in range(y1, y2):
            b, g, r = org_img[y, x]
            new_img[y, x] = lookup_table[g][NEW_I]

    return new_img


def calculate_f_i(last_fi, current_fi, n, k):
    return ((last_fi + current_fi) / 2) * (k / n)


def histogram_equalization(x1, y1, x2, y2, org_img):
    lookup_table = np.zeros((256, 4), dtype=int)
    new_image = org_img
    w, h, bands = org_img.shape
    min_i = 257
    max_i = -1
    k = 256
    n = w * h

    print('histogram equalization')

    # count histogram
    for x in range(x1, x2):
        for y in range(y1, y2):
            b, g, r = org_img[y, x]
            lookup_table[g][H_I] += 1   # count frequency

            if g < min_i:
                min_i = g
            elif g > max_i:
                max_i = g

    print('max i = {}, min i = {}'.format(max_i, min_i))

    # build a lookup table
    for i in range(256):
        if i == 0:
            last_f_i = 0
        else:
            last_f_i = lookup_table[i - 1][F_I]
        current_h_i = lookup_table[i][H_I]
        current_f_i = last_f_i + current_h_i
        lookup_table[i][F_I] = current_f_i
        calculated_f_i = calculate_f_i(last_f_i, current_f_i, n, k)
        lookup_table[i][F_I_CALC] = calculated_f_i
        if calculated_f_i > 255:
            calculated_f_i = 255
        lookup_table[i][FLOOR_F_I_CALC] = math.floor(calculated_f_i)

    print(lookup_table)

    # build a new image
    for x in range(x1, x2):
        for y in range(y1, y2):
            # move pixels
            b, g, r = org_img[y, x]
            new_image[y, x] = lookup_table[g][FLOOR_F_I_CALC]

    return new_image
