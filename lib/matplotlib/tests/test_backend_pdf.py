# -*- encoding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import six

import io
import os

import numpy as np

from matplotlib import cm, rcParams
from matplotlib import pyplot as plt
from matplotlib.testing.decorators import image_comparison, knownfailureif, cleanup

if 'TRAVIS' not in os.environ:
    @image_comparison(baseline_images=['pdf_use14corefonts'], extensions=['pdf'])
    def test_use14corefonts():
        rcParams['pdf.use14corefonts'] = True
        rcParams['font.family'] = 'sans-serif'
        rcParams['font.size'] = 8
        rcParams['font.sans-serif'] = ['Helvetica']
        rcParams['pdf.compression'] = 0

        text = '''A three-line text positioned just above a blue line
    and containing some French characters and the euro symbol:
    "Merci pépé pour les 10 €"'''


@cleanup
def test_type42():
    rcParams['pdf.fonttype'] = 42

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([1, 2, 3])
    fig.savefig(io.BytesIO())


@cleanup
def test_multipage_pagecount():
    from matplotlib.backends.backend_pdf import PdfPages
    from io import BytesIO
    with PdfPages(BytesIO()) as pdf:
        assert pdf.get_pagecount() == 0
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([1, 2, 3])
        fig.savefig(pdf, format="pdf")
        assert pdf.get_pagecount() == 1
        pdf.savefig()
        assert pdf.get_pagecount() == 2
