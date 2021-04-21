"""
"""
import os

import numpy as np
import mne

from meggie_sourceanalysis.datatypes.inverse.inverse import Inverse


def create_default(subject, name, cov=None):
    """ Creates inverse using fsaverage template for source space
    """

    # get fsaverage files
    fs_dir = mne.datasets.fetch_fsaverage(verbose=False)
    subjects_dir = os.path.dirname(fs_dir)

    src = os.path.join(fs_dir, 'bem', 'fsaverage-ico-5-src.fif')
    bem = os.path.join(fs_dir, 'bem', 'fsaverage-5120-5120-5120-bem-sol.fif')
    trans = 'fsaverage'

    raw = subject.get_raw()
    info = raw.info

    # if no cov provided, create a diagonal one
    if not cov: 
        cov = mne.cov.make_ad_hoc_cov(info)

    # compute forward solution
    fwd = mne.make_forward_solution(info, 
                                    trans=trans, 
                                    src=src,
                                    bem=bem,
                                    eeg=True,
                                    meg=True,
                                    mindist=5.0)

    # and then an inverse operator
    inv = mne.minimum_norm.make_inverse_operator(info,
                                                 fwd,
                                                 cov)

    # Create meggie inverse object container
    # and fill it with the inv operator
    inv_directory = subject.inverse_directory
    params = {}
    meggie_inv = Inverse(name, inv_directory, params=params, content=inv)
    meggie_inv.save_content()

    # add to subject
    subject.add(meggie_inv, 'inverse')

