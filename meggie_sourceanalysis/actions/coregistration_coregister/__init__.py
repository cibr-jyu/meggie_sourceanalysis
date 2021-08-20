""" Contains create coregistration action handling.
"""
import os 

from meggie.utilities.names import next_available_name

from meggie.utilities.messaging import exc_messagebox

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.utilities.dialogs.simpleDialogMain import SimpleDialog

from meggie_sourceanalysis.actions.coregistration_coregister.controller.coregistration import coregister_default


class Coregister(Action):
    """ Opens mne coregistration utility.
    """

    def run(self):

        subject = self.experiment.active_subject
        subjects_dir = os.path.join(subject.coregistration_directory, "subjects")

        coreg_name = next_available_name(subject.coregistration.keys(), "Coreg")

        dialog = SimpleDialog(self.experiment, self.window,
                              coreg_name, self.handler, batching=False,
                              title='Create coregistration')
        dialog.show()


    @subject_action
    def handler(self, subject, params):
        """
        """
        coregister_default(self.experiment, self.window, subject, params['name'])

