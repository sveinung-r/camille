"""Camille is a timeseries processing toolbox.

"""

from __future__ import absolute_import

from .processors import fft
from .processors import mooring_fatigue
from .processors import rolling

from .input_loaders import bazefetcher

__version__ = '0.0.1'
