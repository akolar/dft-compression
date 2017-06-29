import numpy as np
######################################################################
#
# Functions to perform fast discrete cosine and sine transforms and
# their inverses in one and two dimensions.  These functions work by
# wrapping the DFT function from numpy, rather than explicitly
# performing the cosine and sine transforms themselves.  The sine
# transforms take arrays whose first element is zero and return arrays
# whose first element is also zero.  This differs from some other
# implementations, which drop the first element, since it is always
# zero.
#
#   dct(y): Type-II discrete cosine transform (DCT) of real data y
#   idct(a): Type-II inverse DCT of a
#   dct2(y): 2D DCT of 2D real array y
#   idct2(a): 2D inverse DCT real array a
#   dst(y): Type-I discrete sine transform (DST) of real data y
#   idst(a): Type-I inverse DST of a
#   dst2(y): 2D DST of 2D real array y
#   idst2(a): 2D inverse DST real array a
#
# Written by Mark Newman <mejn@umich.edu>, June 24, 2011
# You may use, share, or modify this file freely
#
######################################################################


def dct(y):
    n = len(y)
    y2 = np.empty(2 * n, float)
    y2[:n] = y[:]
    y2[n:] = y[::-1]

    c = np.fft.rfft(y2)
    phi = np.exp(-1j * np.pi * np.arange(n) / (2 * n))
    return np.real(phi * c[:n])


def idct(a):
    n = len(a)
    c = np.empty(n + 1, complex)

    phi = np.exp(1j * np.pi * np.arange(n) / (2 * n))
    c[:n] = phi * a
    c[n] = 0.0
    return np.fft.irfft(c)[:n]


def dct2(y):
    m = y.shape[0]
    n = y.shape[1]
    a = np.empty([m, n], float)
    b = np.empty([m, n], float)

    for i in range(m):
        a[i, :] = dct(y[i, :])
    for j in range(n):
        b[:, j] = dct(a[:, j])

    return b


def idct2(b):
    m = b.shape[0]
    n = b.shape[1]
    a = np.empty([m, n], float)
    y = np.empty([m, n], float)

    for i in range(m):
        a[i, :] = idct(b[i, :])
    for j in range(n):
        y[:, j] = idct(a[:, j])

    return y
