import matplotlib.image as mpimg
import numpy as np
from scipy import misc as spm

from dft import aaa, dct


def open_image(path):
    return mpimg.imread(path)


def save_image(image, path, epsilon, delta):
    ttype = 'e:{:0.0f}'.format(epsilon) if epsilon else 'd:{}'.format(delta)

    eidx = path.rfind('.')
    new_path = path[:eidx] + '_{}.conv.jpg'.format(ttype)
    spm.imsave(new_path, image)


def rgb_to_grayscale(image):
    return np.dot(image[..., :3], [0.299, 0.587, 0.114])


def array_map(function, image):
    fn = np.vectorize(function)
    return fn(image)


def convert_rgb(image, epsilon, path):
    r = image[..., 0]
    g = image[..., 1]
    b = image[..., 2]
    cr = convert_channel(r, epsilon)
    cg = convert_channel(g, epsilon)
    cb = convert_channel(b, epsilon)
    s = np.dstack([cr, cg, cb])
    with open(path, 'wb') as f:
        aaa.dump(s, f)
    return s


def convert(image, epsilon, path):
    s = convert_channel(image, epsilon)
    with open(path, 'wb') as f:
        aaa.dump(s, f)
    return s


def convert_channel(image, epsilon):
    transf = dct.dct2(image)
    transf[np.absolute(transf[:, :]) < epsilon] = 0
    return transf


def reverse(spectrum):
    return dct.idct2(spectrum)


def to_image(in_path, out_path):
    with open(in_path, 'rb') as f:
        image = aaa.load(f)

    if len(image.shape) == 2:
        s = dct.idct2(image)
    else:
        cr = dct.idct2(image[..., 0])
        cg = dct.idct2(image[..., 1])
        cb = dct.idct2(image[..., 2])
        s = np.dstack([cr, cg, cb])
    spm.imsave(out_path, s)


def calc_magnitude(image):
    transf = np.fft.fftn(image)
    shifted = np.fft.fftshift(transf)
    return 20 * np.log(np.absolute(transf)), 20 * np.log(np.absolute(shifted))
