import os
import logging

import mne
import numpy as np
import matplotlib.pyplot as plt

from meggie.utilities.decorators import threaded

from meggie_sourceanalysis.datatypes.source_spectrum.source_spectrum import SourceSpectrum


@threaded
def create_source_spectrum(subject, spectrum_name, params, intervals, inv_name):
    """
    """
    logging.getLogger('ui_logger').info('Creating source spectrum!')
