"""Contains implementation for inverse item creation"""

import os

import mne

from meggie_sourceanalysis.datatypes.inverse.inverse import Inverse


def create_inverse(subject, name, cov_name, coreg_name):
    """Creates inverse using fsaverage template for source space"""

    try:
        meggie_coreg = subject.coregistration[coreg_name]
    except Exception:
        raise Exception("Could not find coregistration for subject " + subject.name)

    try:
        meggie_cov = subject.covariance[cov_name]
    except Exception:
        raise Exception("Could not find covariance for subject " + subject.name)

    # get fsaverage files
    subjects_dir = meggie_coreg.subjects_dir
    recon_dir = os.path.join(subjects_dir, subject.name)
    trans_path = meggie_coreg.trans_path

    src = os.path.join(recon_dir, "bem", subject.name + "-ico-5-src.fif")
    bem = os.path.join(recon_dir, "bem", subject.name + "-5120-5120-5120-bem-sol.fif")

    info = subject.get_raw(preload=True).info

    cov = meggie_cov.content

    # compute forward solution
    fwd = mne.make_forward_solution(
        info, trans=trans_path, src=src, bem=bem, eeg=True, meg=True, mindist=5.0
    )

    # and then an inverse operator
    inv = mne.minimum_norm.make_inverse_operator(info, fwd, cov, depth=0.0)

    # Create meggie inverse object container
    # and fill it with the inv operator
    inv_directory = subject.inverse_directory
    params = {
        "lambda2": 0.1,
        "method": "MNE",
        "subjects_dir": subjects_dir,
    }
    meggie_inv = Inverse(name, inv_directory, params=params, content=inv)
    meggie_inv.save_content()

    # add to subject
    subject.add(meggie_inv, "inverse")
