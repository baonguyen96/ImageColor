import cv2
import numpy as np


def ls_transform(x, a, b, A, B):
    tmp = (x - a) * (B - A)
    tmp = tmp / (b - a)
    return tmp + A


def linear_scaling(x1, y1, x2, y2, org_img):
    lookup_table = np.zeros((256, 2), dtype=int)
    new_img = org_img
    min_i = 257
    max_i = -1

    a, b, c = org_img.shape
    print('x1 = {}, y1 = {}, x2 = {}, y2 = {}'.format(x1, y1, x2, y2))
    print('image size = {}x{}'.format(a, b))

    # count histogram
    for y in range(y1, y2):
        for x in range(x1, x2):
            l, u, v = new_img[y, x]
            lookup_table[l][0] += 1  # count frequency

            if l < min_i:
                min_i = l
            elif l > max_i:
                max_i = l

    # build a lookup table
    for i in range(256):
        if min_i <= i <= max_i:
            lookup_table[i][1] = ls_transform(i, min_i, max_i, 0, 255)
        elif i < min_i:
            lookup_table[i][1] = 0
        else:
            lookup_table[i][1] = 255

    w, h, bands = org_img.shape
    for y in range(h - 1):
        for x in range(w - 1):
            b, g, r = org_img[x, y]
            new_img[x, y] = lookup_table[g][1]

    return new_img
