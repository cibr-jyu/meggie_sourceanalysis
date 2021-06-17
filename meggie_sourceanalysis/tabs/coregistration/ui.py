import logging 
import shutil
import os

import mne

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox

from meggie.utilities.decorators import threaded
from meggie.utilities.names import next_available_name

from meggie_sourceanalysis.tabs.coregistration.controller.coregistration import coregister_default


def coregister(experiment, data, window):
    """
    """
    subject = experiment.active_subject
    subjects_dir = os.path.join(subject.coregistration_directory, 'subjects')

    name = next_available_name([], 'Coreg')
    
    coregister_default(window, subject, name)


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
