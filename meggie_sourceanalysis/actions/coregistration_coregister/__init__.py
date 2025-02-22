"""Contains create coregistration action handling."""

import os
import shutil
import mne
import logging

from meggie.utilities.names import next_available_name
from meggie.utilities.threading import threaded

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.utilities.dialogs.simpleDialogMain import SimpleDialog

from meggie_sourceanalysis.datatypes.coregistration.coregistration import Coregistration
from meggie.utilities.messaging import messagebox


class Coregister(Action):
    """Opens mne coregistration utility."""

    def get_trans_path(self, subject, params):
        path = os.path.join(
            self.window.experiment.path,
            subject.name,
            "coregistrations",
            params["name"],
            subject.name + "-trans.fif",
        )
        return path

    def coreg_utility_handler(self, subject, params):
        name = params["name"]

        coreg_dir = os.path.join(subject.coregistration_directory, name)
        subjects_dir = os.path.join(coreg_dir, "subjects")

        # remove existing files
        try:
            shutil.rmtree(coreg_dir)
        except Exception:
            pass

        logging.getLogger("ui_logger").info("Fetching fsaverage..")

        @threaded
        def threaded_fetch():
            return mne.datasets.fetch_fsaverage(verbose=False)

        fs_dir = threaded_fetch(do_meanwhile=self.window.update_ui)

        shutil.copytree(fs_dir, os.path.join(subjects_dir, "fsaverage"))

        # Open the mne coregistration UI
        open_message = (
            "The external coregistration GUI is now open. Please "
            + "align the digitization points with the scalp and then click 'Save' "
            + "in the right panel. Save the transformation file as "
            + self.get_trans_path(subject, params)
            + "."
        )
        messagebox(self.window, open_message)

        logging.getLogger("ui_logger").info("Opening coregistration utility.")
        gui = mne.gui.coregistration(
            inst=subject.raw_path, subject="fsaverage", subjects_dir=subjects_dir
        )

        def close_wrapper(*args, **kwargs):
            if not gui._accept_close_event:
                return
            logging.getLogger("ui_logger").info("Coregistration utility closed.")
            self.handler(subject, params)

            self.window.initialize_ui()

        gui._renderer._window_close_connect(close_wrapper)

    def run(self, params={}):

        subject = self.experiment.active_subject

        coreg_name = next_available_name(subject.coregistration.keys(), "Coreg")

        dialog = SimpleDialog(
            self.experiment,
            self.window,
            coreg_name,
            self.coreg_utility_handler,
            batching=False,
            title="Create coregistration",
        )
        dialog.show()

    @subject_action
    def handler(self, subject, params):
        """ """

        name = params["name"]

        coreg_dir = os.path.join(subject.coregistration_directory, name)
        subjects_dir = os.path.join(coreg_dir, "subjects")

        if not os.path.exists(os.path.join(coreg_dir, subject.name + "-trans.fif")):
            logging.getLogger("ui_logger").info(
                "The coregistration utility was closed without saving, or "
                + "the transformation file was saved to an incorrect location. "
                + "Please ensure the transformation file is saved as "
                + self.get_trans_path(subject, params)
                + "."
            )
            shutil.rmtree(coreg_dir)
            return

        if not os.path.exists(os.path.join(subjects_dir, subject.name)):
            shutil.copytree(
                os.path.join(subjects_dir, "fsaverage"),
                os.path.join(subjects_dir, subject.name),
            )

            for dirpath, _, fnames in reversed(
                list(os.walk(os.path.join(subjects_dir, subject.name)))
            ):
                for fname in fnames:
                    if "fsaverage" in fname:
                        os.rename(
                            os.path.join(dirpath, fname),
                            os.path.join(
                                dirpath, fname.replace("fsaverage", subject.name)
                            ),
                        )
                if "fsaverage" in os.path.basename(dirpath):
                    new_dirpath = os.path.join(
                        os.path.dirname(dirpath),
                        os.path.basename(dirpath).replace("fsaverage", subject.name),
                    )
                    os.rename(dirpath, new_dirpath)

        # And then create a meggie coregistration object.
        params = {}
        path = subject.coregistration_directory
        coreg = Coregistration(name, path, params)
        coreg.save_content()
        subject.add(coreg, "coregistration")
        self.experiment.save_experiment_settings()
