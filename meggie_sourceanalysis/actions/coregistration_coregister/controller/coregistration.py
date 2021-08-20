""" Contains code for wrapping coregistration utility inside Meggie.
"""
import logging
import os
import shutil

import numpy as np
import mne

from meggie.utilities.messaging import messagebox

from meggie_sourceanalysis.datatypes.coregistration.coregistration import Coregistration

from mne.gui import _coreg_gui
original_coreg_close = mne.gui._coreg_gui.CoregFrameHandler.close


def _open_mne_coreg(window, on_close, trans_path, raw_path, 
                    subject_to, subjects_dir):
    """ Opens mne coreg with some small changes.
    """
    # Add on_close handler to coreg GUI with a monkey patch.
    # Pull requests welcome for a proper way.
    def close_wrapper(self, info, is_ok):
        logging.getLogger('ui_logger').info('Coregistration utility closed.')
        on_close()
        return original_coreg_close(self, info, is_ok)
    mne.gui._coreg_gui.CoregFrameHandler.close = close_wrapper

    # To avoid asking user unnecessary questions, we will 
    # also monkey patch two dialogs in mne coreg code.
    save_message = "The coregistration will now be saved. You may close the window when finished."

    class FileDialogWrapper:
        def __init__(self, *args, **kwargs):
            self.return_code = 10
            self.path = trans_path
        def open(self):
            messagebox(window, save_message)
    mne.gui._coreg_gui.FileDialog = FileDialogWrapper

    class NewMriDialogWrapper:
        def __init__(self, *args, **kwrags):
            self.subject_to = subject_to
        
        def edit_traits(self, *args, **kwargs):
            def returnable():
                pass
            returnable.result = True
            return returnable
    mne.gui._coreg_gui.NewMriDialog = NewMriDialogWrapper

    # Open the mne coregistration UI
    open_message = ("An external coregistration GUI is now opened. You should "
                    "fit the digization points to the scalp and then click save "
                    "on the right panel.")
    messagebox(window, open_message)

    logging.getLogger('ui_logger').info('Opening coregistration utility.')
    frame = mne.gui.coregistration(inst=raw_path,
                                   subject='fsaverage',
                                   subjects_dir=subjects_dir)


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
        # In the case that no scaling was done, and no freesurfer subject
        # was created, copy fsaverage directory and rename it properly

        if not os.path.exists(os.path.join(coreg_dir, subject.name + '-trans.fif')):
            logging.getLogger('ui_logger').info('Coregistration utility was closed without saving.')
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

    trans_path = os.path.join(coreg_dir, subject.name + '-trans.fif')
    _open_mne_coreg(window, on_close, trans_path, subject.raw_path, 
                    subject.name, subjects_dir)

