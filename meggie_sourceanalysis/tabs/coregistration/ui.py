import logging 
import shutil
import os

import mne

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox

from meggie.utilities.decorators import threaded
from meggie.utilities.names import next_available_name
from meggie.utilities.dialogs.simpleDialogMain import SimpleDialog

from meggie_sourceanalysis.tabs.coregistration.controller.coregistration import coregister_default


def coregister(experiment, data, window):
    """
    """
    subject = experiment.active_subject
    subjects_dir = os.path.join(subject.coregistration_directory, 'subjects')

    coreg_name = next_available_name(subject.coregistration.keys(), 'Coreg')
    
    def handler(subject, name):
        coregister_default(experiment, window, subject, name)

    dialog = SimpleDialog(experiment, window, coreg_name, handler,
                          title='Create coregistration', batching=False)
    dialog.show()

def delete(experiment, data, window):
    subject = experiment.active_subject
    try:
        selected_name = data['outputs']['coregistration'][0]
    except IndexError as exc:
        return

    try:
        subject.remove(selected_name, 'coregistration')
    except Exception as exc:
        exc_messagebox(window, exc)

    experiment.save_experiment_settings()

    logging.getLogger('ui_logger').info('Deleted coregistration: ' + selected_name)

    window.initialize_ui()


def info(experiment, data, window):
    """
    """
    message = ""
    try:
        selected_name = data['outputs']['coregistration'][0]
        meggie_coreg = experiment.active_subject.coregistration[selected_name]

        message += "Name: " + meggie_coreg.name + "\n\n"
    except Exception as exc:
        message = ""

    return message
