""" Contains functions for handling noise covariance matrices.
"""
import os

import numpy as np
import mne

from meggie_sourceanalysis.datatypes.covariance.covariance import Covariance


def create_covariance(subject, name):
    """ Creates covariance based on dialog inputs.
    """

