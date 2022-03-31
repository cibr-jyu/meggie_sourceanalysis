""" Contains code for wrapping coregistration utility inside Meggie.
"""
import logging
import os
import shutil

import numpy as np
import mne

from meggie.utilities.messaging import messagebox

from meggie_sourceanalysis.datatypes.coregistration.coregistration import Coregistration


def _open_mne_coreg(window, on_close, raw_path, 
                    subjects_dir):
    """ Opens mne coreg with some small changes.
    """

    # Open the mne coregistration UI
    open_message = ("An external coregistration GUI is now opened. You should "
                    "fit the digization points to the scalp and then click save "
                    "on the right panel. The trans file should be saved as "
                    "`experiment_folder`/`subject_name`/coregistrations/"
                    "`coreg_name`/`subject_name`-trans.fif")
    messagebox(window, open_message)

    logging.getLogger('ui_logger').info('Opening coregistration utility.')
    gui = mne.gui.coregistration(inst=raw_path,
                                 subject='fsaverage',
                                 subjects_dir=subjects_dir)

    def close_wrapper(*args, **kwargs):
        if not gui._accept_close_event:
            return
        logging.getLogger('ui_logger').info('Coregistration utility closed.')
        on_close()
    gui._renderer._window_close_connect(close_wrapper)


def coregister_default(experiment, window, subject, name):

    coreg_dir = os.path.join(subject.coregistration_directory, name)
    subjects_dir = os.path.join(coreg_dir, 'subjects')

    # remove existing files
    try:
        shutil.rmtree(coreg_dir)
    except Exception as exc:
        pass

    logging.getLogger('ui_logger').info('Fetching fsaverage..')
    fs_dir = mne.datasets.fetch_fsaverage(verbose=False)
    shutil.copytree(fs_dir, os.path.join(subjects_dir, 'fsaverage'))

    def on_close():

        if not os.path.exists(os.path.join(coreg_dir, subject.name + '-trans.fif')):
            logging.getLogger('ui_logger').info(
                "Coregistration utility was closed without saving or "
                "the trans file was saved to a wrong location. "
                "The trans file should be saved as "
                "`experiment_folder`/`subject_name`/coregistrations/"
                "`coreg_name`/`subject_name`-trans.fif")
            shutil.rmtree(coreg_dir)
            return

        if not os.path.exists(os.path.join(subjects_dir, subject.name)):
            shutil.copytree(os.path.join(subjects_dir, 'fsaverage'),
                            os.path.join(subjects_dir, subject.name))

            for dirpath, _, fnames in reversed(list(os.walk(os.path.join(subjects_dir, subject.name)))):
                for fname in fnames:
                    if 'fsaverage' in fname:
                        os.rename(os.path.join(dirpath, fname),
                                  os.path.join(dirpath, fname.replace('fsaverage', subject.name)))
                if 'fsaverage' in os.path.basename(dirpath):
                    new_dirpath = os.path.join(os.path.dirname(dirpath),
                                               os.path.basename(dirpath).replace('fsaverage', subject.name))
                    os.rename(dirpath, new_dirpath)

        # And then create a meggie coregistration object.
        params = {}
        path = subject.coregistration_directory
        coreg = Coregistration(name, path, params)
        coreg.save_content()
        subject.add(coreg, 'coregistration')

        experiment.save_experiment_settings()
        window.initialize_ui()

    _open_mne_coreg(window, on_close, subject.raw_path, 
                    subjects_dir)

