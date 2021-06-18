import logging 
import os

import mne

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox

from meggie_sourceanalysis.tabs.inverse.controller.inverse import create_inverse

from meggie.utilities.dialogs.simpleDialogMain import SimpleDialog

from meggie.utilities.decorators import threaded
from meggie.utilities.names import next_available_name


def plot_alignment(experiment, data, window):
    """ Creates a plot for inspecting the goodness of alignment between
    the data frame and the default template
    """
    subject = experiment.active_subject

    raw = subject.get_raw(preload=False)

    fs_dir = mne.datasets.fetch_fsaverage(verbose=False)
    subjects_dir = os.path.dirname(fs_dir)

    logging.getLogger('ui_logger').info('Plotting alignment..')

    mne.viz.plot_alignment(info=raw.info,
                           trans='fsaverage',
                           subject='fsaverage',
                           subjects_dir=subjects_dir,
                           meg='helmet',
                           eeg='projected')


def create(experiment, data, window):
    """
    """
    active_subject = experiment.active_subject

    invs = active_subject.inverse.keys()
    inv_name = next_available_name(invs, 'Inv')

    try:
        cov_name = data['inputs']['covariance'][0]
    except IndexError as exc:
        return

    try:
        coreg_name = data['inputs']['coregistration'][0]
    except IndexError as exc:
        return

    def handler(subject, name):
        @threaded
        def threaded_create():
            try:
                create_inverse(subject, name, cov_name, coreg_name)
                logging.getLogger('ui_logger').info('Created inverse with name ' + name)
            except Exception as exc:
                logging.getLogger('ui_logger').exception('')

        threaded_create(do_meanwhile=window.update_ui)

    dialog = SimpleDialog(experiment, window, inv_name, handler,
                          title='Create inverse', batching=True)
    dialog.show()


def delete(experiment, data, window):
    """ 
    """
    subject = experiment.active_subject
    try:
        selected_name = data['outputs']['inverse'][0]
    except IndexError as exc:
        return

    try:
        subject.remove(selected_name, 'inverse')
    except Exception as exc:
        exc_messagebox(window, exc)

    experiment.save_experiment_settings()

    logging.getLogger('ui_logger').info('Deleted inverse: ' + selected_name)

    window.initialize_ui()


def info(experiment, data, window):
    """
    """
    message = ""
    try:
        selected_name = data['outputs']['inverse'][0]
        meggie_inv = experiment.active_subject.inverse[selected_name]

        inv = meggie_inv.content

        message += "Name: " + str(meggie_inv.name) + "\n\n"

        message += "Based on trans: " + os.path.basename(inv['info']['mri_file']) + '\n\n'

        message += "Source space: \n"
        message += "LH: " + str(len(inv['src'][0]['vertno'])) + ' vertices' + '\n'
        message += "RH: " + str(len(inv['src'][1]['vertno'])) + ' vertices' + '\n'

        message += "\n"

        message += "lambda2: " + str(meggie_inv.params['lambda2']) + "\n"
        message += "Method: " + str(meggie_inv.params['method']) + "\n"

    except Exception as exc:
        message = ""
    return message

