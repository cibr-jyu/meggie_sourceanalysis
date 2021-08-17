""" Contains create covariance action handling.
"""
import os 

import mne

from meggie.utilities.names import next_available_name

from meggie.utilities.messaging import exc_messagebox

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie_sourceanalysis.datatypes.covariance.covariance import Covariance

from meggie.utilities.dialogs.simpleDialogMain import SimpleDialog


class CreateCovariance(Action):
    """ Creates ad hoc covariance items
    """

    def run(self):

        subject = self.experiment.active_subject

        covs = subject.covariance.keys()
        cov_name = next_available_name(covs, "Cov")

        dialog = SimpleDialog(self.experiment, self.window,
                              cov_name, self.handler, title='Create covariance')
        dialog.show()


    @subject_action
    def handler(self, subject, params):
        """
        """
        info = subject.get_raw(preload=False).info
        cov = mne.cov.make_ad_hoc_cov(info)

        meggie_cov = Covariance(params['name'],
                                subject.covariance_directory,
                                {},
                                content=cov)
        meggie_cov.save_content()
        subject.add(meggie_cov, "covariance")

        self.window.initialize_ui()

