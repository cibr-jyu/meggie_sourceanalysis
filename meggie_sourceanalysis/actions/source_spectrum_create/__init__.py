""" Contains create spectrum action handling.
"""
import os 

from meggie.utilities.names import next_available_name

from meggie.utilities.messaging import exc_messagebox

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.utilities.dialogs.powerSpectrumDialogMain import PowerSpectrumDialog

from meggie_sourceanalysis.actions.source_spectrum_create.controller.source_spectrum import create_source_spectrum


class CreateSpectrum(Action):
    """ Creates source spectrum items.
    """

    def run(self):

        subject = self.experiment.active_subject

        default_name = next_available_name(subject.source_spectrum.keys(), "Spectrum")

        try:
            inv_name = self.data['inputs']['inverse'][0]
        except IndexError as exc:
            return

        def handle_subject(subject, params):
            params['inv_name'] = inv_name
            self.handler(subject, params)

        dialog = PowerSpectrumDialog(self.experiment, self.window,
                                     default_name, handler=handle_subject)
        dialog.show()


    @subject_action
    def handler(self, subject, params):
        """
        """
        create_source_spectrum(subject, params, 
                               do_meanwhile=self.window.update_ui)

