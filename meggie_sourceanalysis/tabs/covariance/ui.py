import logging 
import os

import mne

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox

from meggie_sourceanalysis.tabs.covariance.controller.covariance import create_covariance

from meggie.utilities.decorators import threaded
from meggie.utilities.names import next_available_name


def create(experiment, data, window):
    """
    """
    active_subject = experiment.active_subject

    covs = active_subject.covariance.keys()
    name = next_available_name(covs, 'Cov')

    logging.getLogger('ui_logger').info('Create clicked')


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

