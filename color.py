import numpy as np
from collections import Counter


# constants
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


def bgr2xyz(bgr_image):
    xyz_image = bgr_image
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
            new_pixel_value = rgb2xyz_matrix * bgr_matrix
            xyz_image[x, y] = new_pixel_value.transpose()

    return xyz_image


def xyz2bgr(xyz_image):
    bgr_image = xyz_image
    w, h, bands = xyz_image.shape
    for y in range(0, h):
        for x in range(0, w):
            # linear bgr
            x_val, y_val, z_val = xyz_image[x, y]
            xyz_matrix = np.matrix('{} {} {}'.format(x_val, y_val, z_val)).transpose()
            new_pixel_value = xyz2rgb_matrix * xyz_matrix  # rgb form
            r = new_pixel_value.item(0)
            g = new_pixel_value.item(1)
            b = new_pixel_value.item(2)

            # convert to nonlinear bgr
            r = gamma(r)
            g = gamma(g)
            b = gamma(b)
            new_pixel_value = np.matrix('{} {} {}'.format(b, g, r))  # bgr form
            bgr_image[x, y] = new_pixel_value

    return bgr_image


# working on this
def xyz2luv(xyz_image):
    luv_image = xyz_image
    w, h, bands = xyz_image.shape
    for y in range(0, h):
        for x in range(0, w):
            x_value, y_value, z_value = xyz_image[x, y]

            # compute t and l (l should be between 0 and 100)
            t = y_value / yw
            if t > 0.008856:
                l = 116 * (t ** (1 / 3)) - 16
            else:
                l = 903.3 * t

            # compute u, v
            d = x_value + 15 * y_value + 3 * z_value
            if d == 0:
                u_prime = v_prime = 0
            else:
                u_prime = 4 * x_value / d
                v_prime = 9 * y_value / d
            u = 12 * l * (u_prime - uw)
            v = 13 * l * (v_prime - vw)

            # store luv pixel
            luv_pixel = np.matrix('{} {} {}'.format(l, u, v))
            luv_image[x, y] = luv_pixel

    return luv_image


def luv2xyz(luv_image):
    xyz_image = luv_image
    w, h, bands = xyz_image.shape
    for y in range(0, h):
        for x in range(0, w):
            l, u, v = luv_image[x, y]

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
                x_value = y * 2.25 * (u_prime / v_prime)
                z_value = y * (3 - 0.75 * u_prime - 5 * v_prime) / v_prime

            # store xyz pixel
            xyz_pixel = np.matrix('{} {} {}'.format(x_value, y_value, z_value))
            xyz_image[x, y] = xyz_pixel

    return xyz_image


def bgr2luv(bgr_image):
    # nonlinear bgr
    bgr_image = bgr_image * 1. / 255

    # bgr to xyz
    xyz_image = bgr2xyz(bgr_image)

    # xyz to luv
    luv_image = xyz2luv(xyz_image)

    return luv_image


def luv2bgr(luv_img):
    # luv to xyz
    xyz_image = luv2xyz(luv_img)

    # xyz to bgr
    bgr_image = xyz2bgr(xyz_image)

    # convert to bgr8
    bgr_image = bgr_image * 255

    return bgr_image


def linear_scaling(x1, y1, x2, y2, rgb_img):
    histogram_index_value = []
    min_i = 257
    max_i = -1

    w, h, b = rgb_img.shape
    # print('x1 = {}, y1 = {}, x2 = {}, y2 = {}'.format(x1, y1, x2, y2))
    # print('image size = {}x{}'.format(w, h))

    # rgb -> luv
    luv_image = bgr2luv(rgb_img)

    # count histogram
    # for y in range(y1, y2):
    #     for x in range(x1, x2):
    #         l, u, v = luv_image[y, x]
    #         histogram_index_value += [str.format("%.6f" % l)]
    #
    #         if l < min_i:
    #             min_i = l
    #         elif l > max_i:
    #             max_i = l
    # histogram_count_index_value = Counter(histogram_index_value)
    # new_i = histogram_count_index_value
    #
    # # build a lookup table
    # for y in range(y1, y2):
    #     for x in range(x1, x2):
    #         l, u, v = luv_image[y, x]
    #         l_as_str = str.format("%.6f" % l)
    #         new_i[l_as_str] = ls_transform(l, min_i, max_i, 0, 100)
    #
    # # build new image using linear scaling in luv
    # scaled_luv_image = luv_image
    # for y in range(h):
    #     for x in range(w):
    #         l, u, v = luv_image[x, y]
    #         l_as_str = str.format("%.6f" % l)
    #         new_luv_matrix = np.matrix('{} {} {}'.format(
    #             new_i[l_as_str], u, v
    #         ))
    #         scaled_luv_image[x, y] = new_luv_matrix

    # luv -> bgr
    bgr_img = luv2bgr(luv_image)     # weird result numbers

    return bgr_img
