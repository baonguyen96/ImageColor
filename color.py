"""
Bao Nguyen
BCN140030
CS 4391.001
"""

import numpy as np
import math


########################################################################
#  constants
rgb2xyz_matrix = np.matrix(
    '0.412453 0.357580 0.180423; '
    '0.212671 0.715160 0.072169; '
    '0.019334 0.119193 0.950227'
)

xyz2rgb_matrix = np.matrix(
    '3.2404790 -1.537150 -0.498535; '
    '-0.969256 1.8759910 0.041556; '
    '0.0556480 -0.204043 1.057311'
)

xw = 0.95
yw = 1
zw = 1.09
uw = (4 * xw) / (xw + 15 * yw + 3 * zw)
vw = (9 * yw) / (xw + 15 * yw + 3 * zw)
########################################################################


def ls_transform(x, a, b, A, B):
    tmp = (x - a) * (B - A)
    tmp = tmp / (b - a)
    return tmp + A


def inverse_gamma(v):
    if v < 0.03928:
        result = v / 12.92
    else:
        result = ((v + 0.055) ** 2.4) / 1.055
    return result


def gamma(d):
    if d < 0.00304:
        result = d * 12.92
    else:
        result = (1.055 * (d ** (1 / 2.4))) - 0.055
    return result


def calculate_fi(last_fi, current_fi, n, k):
    return ((last_fi + current_fi) / 2) * (k / n)


def bgr2luv(bgr_image):
    # nonlinear bgr
    bgr_image = bgr_image * 1. / 255

    luv_image = bgr_image.copy()
    w, h, band = bgr_image.shape

    # bgr to xyz
    for y in range(0, h):
        for x in range(0, w):
            b, g, r = bgr_image[x, y]

            # linear bgr
            b = inverse_gamma(b)
            g = inverse_gamma(g)
            r = inverse_gamma(r)
            bgr_matrix = np.matrix('{} {} {}'.format(r, g, b)).transpose()

            # bgr -> xyz pixel
            xyz_pixel_value = rgb2xyz_matrix * bgr_matrix
            xyz_pixel_value = xyz_pixel_value.transpose()

            ##############

            # xyz -> luv pixel
            x_value = xyz_pixel_value.item(0)
            y_value = xyz_pixel_value.item(1)
            z_value = xyz_pixel_value.item(2)

            # compute t and l (l should be between 0 and 100)
            t = y_value / yw
            l = 0
            if t > 0.008856:
                l = 116 * (t ** (1 / 3)) - 16
            else:
                l = 903.3 * t

            # compute u, v (set u' and v' are 0 if d = 0 to protect against divide by 0)
            d = x_value + 15 * y_value + 3 * z_value
            if d == 0:
                u_prime = v_prime = 0
            else:
                u_prime = (4 * x_value) / d
                v_prime = (9 * y_value) / d
            u = 13 * l * (u_prime - uw)
            v = 13 * l * (v_prime - vw)

            # store luv pixel
            luv_pixel = np.matrix('{} {} {}'.format(l, u, v))
            luv_image[x, y] = luv_pixel

    return luv_image


def luv2bgr(luv_image):
    # luv to xyz
    xyz_image = luv_image.copy()
    bgr_image = luv_image.copy()
    w, h, bands = xyz_image.shape
    for y in range(0, h):
        for x in range(0, w):
            l, u, v = luv_image[x, y]

            # prevent divide by 0
            if l == 0:
                u_prime = v_prime = 0
            else:
                u_prime = (u + 13 * uw * l) / (13 * l)
                v_prime = (v + 13 * vw * l) / (13 * l)

            # compute y value from l
            if l > 7.9996:
                y_value = (((l + 16) / 116) ** 3) * yw
            else:
                y_value = (l / 903.3) * yw

            # compute z value from y value
            if v_prime == 0:
                x_value = 0
                z_value = 0
            else:
                x_value = y_value * 2.25 * (u_prime / v_prime)
                z_value = y_value * (3 - 0.75 * u_prime - 5 * v_prime) / v_prime

            ########################

            # xyz to linear bgr
            xyz_matrix = np.matrix('{} {} {}'.format(x_value, y_value, z_value)).transpose()
            new_pixel_value = xyz2rgb_matrix * xyz_matrix  # rgb form

            # convert to nonlinear bgr
            r = gamma(new_pixel_value.item(0))
            g = gamma(new_pixel_value.item(1))
            b = gamma(new_pixel_value.item(2))
            new_pixel_value = np.matrix('{} {} {}'.format(b, g, r))  # bgr form
            bgr_image[x, y] = new_pixel_value

    # convert to bgr8
    bgr_image = bgr_image * 255

    return bgr_image


def linear_scaling(x1, y1, x2, y2, rgb_img):
    print('Applying linear scaling...')

    min_l = 257
    max_l = -1
    w, h, bands = rgb_img.shape

    # rgb -> luv
    luv_image = bgr2luv(rgb_img)
    scaled_luv_image = luv_image.copy()

    # count histogram
    for y in range(y1, y2):
        for x in range(x1, x2):
            l, u, v = luv_image[y, x]
            if l < min_l:
                min_l = l
            elif l > max_l:
                max_l = l

    # build new image using linear scaling in luv
    for y in range(h):
        for x in range(w):
            l, u, v = luv_image[x, y]

            if l < min_l:
                l = 0
            elif l > max_l:
                l = 100
            else:
                l = ls_transform(l, min_l, max_l, 0, 100)

            new_luv_matrix = np.matrix('{} {} {}'.format(l, u, v))
            scaled_luv_image[x, y] = new_luv_matrix

    # luv -> bgr
    bgr_img = luv2bgr(scaled_luv_image)

    print('Complete applying linear scaling')

    return bgr_img


def histogram_equalization(x1, y1, x2, y2, rgb_img):
    print('Applying histogram equalization...')

    # lookup table columns
    hi_col = 0
    fi_col = 1
    fi_calc_col = 2
    floor_fi_calc_col = 3

    w, h, bands = rgb_img.shape
    min_l = 101
    max_l = -1
    k = 101
    n = (x2 - x1) * (y2 - y1)
    lookup_table = np.zeros((105, 4), dtype=float)

    # rgb -> luv
    luv_image = bgr2luv(rgb_img)
    scaled_luv_image = luv_image.copy()

    # count histogram
    for y in range(y1, y2):
        for x in range(x1, x2):
            l, u, v = luv_image[y, x]

            # discretization of L value
            lookup_table[int(round(l))] += 1

            if l < min_l:
                min_l = l
            elif l > max_l:
                max_l = l

    # build a lookup table for Luv
    for index in range(101):
        # calculate cumulative histogram, different for first element
        if index == 0:
            last_fi = 0
        else:
            last_fi = lookup_table[index - 1][fi_col]

        # compute values and update lookup table
        current_hi = lookup_table[index][hi_col]
        current_fi = last_fi + current_hi
        lookup_table[index][fi_col] = current_fi
        calculated_fi = calculate_fi(last_fi, current_fi, n, k)
        lookup_table[index][fi_calc_col] = calculated_fi
        if calculated_fi > 100:
            calculated_fi = 100
        lookup_table[index][floor_fi_calc_col] = math.floor(calculated_fi)

    # build new image using histogram equalization in luv
    for y in range(h):
        for x in range(w):
            l, u, v = luv_image[x, y]

            if l < min_l:
                l = 0
            elif l > max_l:
                l = 100
            else:
                l = lookup_table[int(round(l))][floor_fi_calc_col]

            new_luv_matrix = np.matrix('{} {} {}'.format(l, u, v))
            scaled_luv_image[x, y] = new_luv_matrix

    # luv -> bgr
    bgr_img = luv2bgr(scaled_luv_image)

    print('Complete applying histogram equalization')

    return bgr_img
