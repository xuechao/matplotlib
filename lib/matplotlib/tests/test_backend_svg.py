from __future__ import absolute_import, division, print_function, unicode_literals

import six

import numpy as np
from io import BytesIO
import xml.parsers.expat

import matplotlib.pyplot as plt
from matplotlib.testing.decorators import cleanup
from matplotlib.testing.decorators import image_comparison


@cleanup
def test_visibility():
    fig = plt.figure()
    ax = fig.add_subplot(111)

    x = np.linspace(0, 4 * np.pi, 50)
    y = np.sin(x)
    yerr = np.ones_like(y)

    a, b, c = ax.errorbar(x, y, yerr=yerr, fmt='ko')
    for artist in b:
        artist.set_visible(False)

    fd = BytesIO()
    fig.savefig(fd, format='svg')

    fd.seek(0)
    buf = fd.read()
    fd.close()

    parser = xml.parsers.expat.ParserCreate()
    parser.Parse(buf)  # this will raise ExpatError if the svg is invalid


@image_comparison(baseline_images=['noscale'], remove_text=True)
def test_noscale():
    X, Y = np.meshgrid(np.arange(-5, 5, 1), np.arange(-5, 5, 1))
    Z = np.sin(Y ** 2)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(Z, cmap='gray')
    plt.rcParams['svg.image_noscale'] = True


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)
