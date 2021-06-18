import logging 
import os

import mne

from meggie_sourceanalysis.datatypes.covariance.covariance import Covariance

from meggie.utilities.dialogs.simpleDialogMain import SimpleDialog

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox

from meggie.utilities.decorators import threaded
from meggie.utilities.names import next_available_name


def create_ad_hoc(experiment, data, window):
    """
    """
    active_subject = experiment.active_subject

    covs = active_subject.covariance.keys()
    cov_name = next_available_name(covs, 'Cov')

    def handler(subject, name):
        info = subject.get_raw(preload=False).info
        cov = mne.cov.make_ad_hoc_cov(info)

        meggie_cov = Covariance(name, 
                                subject.covariance_directory, 
                                {}, 
                                content=cov)
        meggie_cov.save_content()
        subject.add(meggie_cov, 'covariance')

    dialog = SimpleDialog(experiment, window, cov_name, handler,
                          title='Create ad hoc covariance')
    dialog.show()


def delete(experiment, data, window):
    """ 
    """
    subject = experiment.active_subject
    try:
        selected_name = data['outputs']['covariance'][0]
    except IndexError as exc:
        return

    try:
        subject.remove(selected_name, 'covariance')
    except Exception as exc:
        exc_messagebox(window, exc)

    experiment.save_experiment_settings()

    logging.getLogger('ui_logger').info('Deleted covariance: ' + selected_name)

    window.initialize_ui()


def info(experiment, data, window):
    """
    """
    message = ""
    try:
        selected_name = data['outputs']['covariance'][0]
        meggie_cov = experiment.active_subject.covariance[selected_name]

        cov = meggie_cov.content

        message += "Name: " + str(meggie_cov.name) + "\n\n"

    except Exception as exc:
        message = ""
    return message

