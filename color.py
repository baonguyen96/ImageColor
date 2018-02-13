import numpy as np

# constants
rgb2xyz_matrix = np.matrix(
    '0.412453 0.357580 0.180423; '
    '0.212671 0.715160 0.072169; '
    '0.019334 0.119193 0.950227'
)

xyz2rgb_matrix = np.matrix(
    '3.240479 -1.53715 -0.498525;'
    '-0.969256 1.875991 0.041556;'
    '0.055648 -0.204043 1.057311'
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
        result = ((1.055 * d) ** (1 / 2.4)) - 0.055
    return result


def bgr2xyz(bgr_image):
    xyz_image = np.zeros(bgr_image.shape, dtype=np.object)
    w, h, band = bgr_image.shape

    # print('rgb2xyz_matrix')
    # print(rgb2xyz_matrix)
    # print()
    # print('bgr_image')
    # print(bgr_image)
    # print()

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

    # print('xyz_image')
    # print(xyz_image)
    # print()

    return xyz_image


def xyz2bgr(xyz_image):
    bgr_image = np.zeros(xyz_image.shape, dtype=np.object)
    w, h, bands = xyz_image.shape
    for y in range(0, h):
        for x in range(0, w):
            # linear bgr
            x_val, y_val, z_val = xyz_image[x, y]
            xyz_matrix = np.matrix('{} {} {}'.format(x_val, y_val, z_val)).transpose()
            new_pixel_value = xyz2rgb_matrix * xyz_matrix  # rgb form
            r = new_pixel_value[0]
            g = new_pixel_value[1]
            b = new_pixel_value[2]

            # convert to nonlinear bgr
            r = gamma(r)
            g = gamma(g)
            b = gamma(b)
            new_pixel_value = np.matrix(b, g, r)  # bgr form
            bgr_image[x, y] = new_pixel_value.transpose()

    return bgr_image


# working on this
def xyz2luv(xyz_image):
    luv_image = np.zeros(xyz_image.shape, dtype=np.object)
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
    xyz_image = np.zeros(luv_image.shape, dtype=np.object)
    w, h, bands = xyz_image.shape
    for y in range(0, h):
        for x in range(0, w):
            l, u, v = luv_image[x, y]

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

    # print('xyz_image')
    # print(xyz_image)
    # print()
    # print('bgr_image')
    # print(bgr_image)
    # print()

    return bgr_image


def linear_scaling(x1, y1, x2, y2, rgb_img):
    lookup_table = np.zeros((256, 2), dtype=int)
    min_i = 257
    max_i = -1

    w, h, b = rgb_img.shape
    print('x1 = {}, y1 = {}, x2 = {}, y2 = {}'.format(x1, y1, x2, y2))
    print('image size = {}x{}'.format(w, h))

    # rgb -> luv
    luv_image = bgr2luv(rgb_img)

    # count histogram
    for y in range(y1, y2):
        for x in range(x1, x2):
            l, u, v = luv_image[y, x]
            lookup_table[l][0] += 1  # count frequency, l needs to be integer but here it is not

            if l < min_i:
                min_i = l
            elif l > max_i:
                max_i = l

    # build a lookup table
    for i in range(100):
        if min_i <= i <= max_i:
            lookup_table[i][1] = ls_transform(i, min_i, max_i, 0, 100)
        elif i < min_i:
            lookup_table[i][1] = 0
        else:
            lookup_table[i][1] = 100

    # build new image using linear scaling in luv
    scaled_luv_image = luv_image
    for y in range(h):
        for x in range(w):
            l, u, v = luv_image[x, y]
            scaled_luv_image[x, y] = lookup_table[l][1]

    # luv -> bgr
    bgr_img = luv2bgr(scaled_luv_image)

    return bgr_img
