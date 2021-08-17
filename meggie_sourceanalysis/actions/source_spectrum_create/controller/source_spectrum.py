""" Contains implementation for creating source spectrums
"""
import os
import logging

from copy import deepcopy
from collections import OrderedDict

import mne
import numpy as np
import matplotlib.pyplot as plt

from meggie_sourceanalysis.datatypes.source_spectrum.source_spectrum import SourceSpectrum

from meggie.utilities.threading import threaded
from meggie.utilities.events import get_raw_blocks_from_intervals


@threaded
def create_source_spectrum(subject, params):
    """ Creates source spectrum items.
    """
    spectrum_name = params['name']
    intervals = params['intervals']
    inv_name = params['inv_name']

    fmin = params['fmin']
    fmax = params['fmax']
    nfft = params['nfft']
    overlap = params['overlap'] / float(nfft)

    # get raw objects organized with average groups as keys
    ival_times, raw_block_groups = get_raw_blocks_from_intervals(subject,
                                                                 intervals)

    raw = subject.get_raw()
    info = raw.info

    try:
        meggie_inv = subject.inverse[inv_name]
    except KeyError as exc:
        raise Exception("Missing " + inv_name)

    inv = meggie_inv.content

    picks = mne.pick_types(info, meg=True, eeg=True,
                           exclude='bads')

    lambda2 = meggie_inv.params.get('lambda2', 0.1)
    method = meggie_inv.params.get('method', 'dSPM')

    # compute psd's
    psd_groups = OrderedDict()
    for key, raw_blocks in raw_block_groups.items():
        for raw_block in raw_blocks:
            length = len(raw_block.times)
            stc_psd = mne.minimum_norm.compute_source_psd(
                raw_block, inv, lambda2=lambda2, method=method,
                fmin=fmin, fmax=fmax, n_fft=nfft, overlap=overlap,
                pick_ori=None, dB=False, return_sensor=False, verbose=False)

            freqs = stc_psd.times

            if key not in psd_groups:
                psd_groups[key] = []

            psd_groups[key].append((stc_psd, freqs, length))

    for psd_list in psd_groups.values():
        freqs = psd_list[0][1]
        vertices = psd_list[0][0].vertices
        fs_subject = psd_list[0][0].subject
        break

    psds = []
    for psd_list in psd_groups.values():
        # do a weighted (raw block lengths as weights) average of psds inside a
        # group
        weights = np.array([length for stc, freqs, length in psd_list])
        weights = weights.astype(float) / np.sum(weights)
        stc_data = np.average([stc.data for stc, freqs, length in psd_list],
                              weights=weights, axis=0)

        stc_psd = mne.SourceEstimate(stc_data,
                                     vertices,
                                     tmin=freqs[0],
                                     tstep=(freqs[1]-freqs[0]),
                                     subject=fs_subject)
        psds.append(stc_psd)

    psd_data = dict(zip(psd_groups.keys(), psds))

    params = deepcopy(params)
    params['conditions'] = [elem for elem in psd_groups.keys()]
    params['intervals'] = ival_times
    params['fs_subject'] = fs_subject
    params['subjects_dir'] = meggie_inv.params['subjects_dir']

    spectrum = SourceSpectrum(spectrum_name, subject.source_spectrum_directory,
                              params, psd_data)

    spectrum.save_content()
    subject.add(spectrum, 'source_spectrum')

