""" Contains create inverse action handling.
"""
import os 

from meggie.utilities.names import next_available_name
from meggie.utilities.threading import threaded

from meggie.utilities.messaging import exc_messagebox

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.utilities.dialogs.simpleDialogMain import SimpleDialog

from meggie_sourceanalysis.actions.inverse_create.controller.inverse import create_inverse


class CreateInverse(Action):
    """ Creates inverse items based on covariances and coregistrations
    """

    def run(self):

        subject = self.experiment.active_subject

        inv_name = next_available_name(subject.inverse.keys(), "Inv")

        try:
            cov_name = self.data['inputs']['covariance'][0]
        except IndexError as exc:
            return

        try:
            coreg_name = self.data['inputs']['coregistration'][0]
        except IndexError as exc:
            return

        def handle_subject(subject, params):
            params['cov_name'] = cov_name
            params['coreg_name'] = coreg_name
            self.handler(subject, params)

        dialog = SimpleDialog(self.experiment, self.window,
                              inv_name, handle_subject, title='Create inverse')
        dialog.show()


    @subject_action
    def handler(self, subject, params):
        """
        """
        @threaded
        def threaded_create():
            create_inverse(subject, params['name'], params['cov_name'],
                           params['coreg_name'])
        threaded_create(do_meanwhile=self.window.update_ui)

