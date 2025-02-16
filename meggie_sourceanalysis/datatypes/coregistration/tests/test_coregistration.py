import tempfile
import shutil
import os

import mne

from meggie_sourceanalysis.datatypes.coregistration.coregistration import Coregistration

from meggie.utilities.filemanager import ensure_folders


def test_coregistration():
    with tempfile.TemporaryDirectory() as dirpath:

        # get trans file
        sample_folder = mne.datasets.sample.data_path()
        sample_trans_fname = os.path.join(
            sample_folder, "MEG", "sample", "sample_audvis_raw-trans.fif"
        )

        # get mri data
        fs_dir = mne.datasets.fetch_fsaverage(verbose=False)

        # create destination folders
        sample_dir = os.path.join(dirpath, "sample_audvis_raw")
        coregistrations_dir = os.path.join(sample_dir, "coregistrations")
        coreg_dir = os.path.join(coregistrations_dir, "CoregTest")
        subjects_dir = os.path.join(coreg_dir, "subjects")
        ensure_folders([subjects_dir])

        # copy trans file under the coreg folder
        shutil.copy(sample_trans_fname, coreg_dir)

        # copy fsaverage mri files under the subjects folder
        shutil.copytree(fs_dir, os.path.join(subjects_dir, "fsaverage"))

        coreg = Coregistration("CoregTest", coregistrations_dir, {})

        # Creating Coreg object with same name and folder should allow
        # accessing the content
        loaded_coreg = Coregistration("CoregTest", coregistrations_dir, {})

        assert loaded_coreg.trans_path == coreg.trans_path
