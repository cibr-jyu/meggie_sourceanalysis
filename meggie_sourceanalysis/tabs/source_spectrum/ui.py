import logging 

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.names import next_available_name

from meggie.utilities.dialogs.powerSpectrumDialogMain import PowerSpectrumDialog

from meggie_sourceanalysis.tabs.source_spectrum.controller.source_spectrum import create_source_spectrum


def delete(experiment, data, window):
    """ 
    """
    subject = experiment.active_subject
    try:
        selected_name = data['outputs']['source_spectrum'][0]
    except IndexError as exc:
        return

    try:
        subject.remove(selected_name, 'source_spectrum')
    except Exception as exc:
        exc_messagebox(window, exc)

    experiment.save_experiment_settings()

    logging.getLogger('ui_logger').info('Deleted source spectrum')
    window.initialize_ui()


def create(experiment, data, window):
    """ Uses spectrum creation dialog from core meggie
    """
    default_name = next_available_name(
        experiment.active_subject.source_spectrum.keys(), 'Spectrum')
     
    try:
        inv_name = data['inputs']['inverse'][0]
    except Exception as exc:
        messagebox(window, 'Inverse need to be selected for computing source spectrums')
        return

    def handler(subject, spectrum_name, params, intervals):
        """ Handles spectrum creation, initiated by the dialog
        """
        create_source_spectrum(subject, spectrum_name, params, intervals, inv_name,
                               do_meanwhile=window.update_ui)

    dialog = PowerSpectrumDialog(experiment, window, default_name, handler=handler)
    dialog.show()


def plot_spectrum(experiment, data, window):
    """ 
    """

def info(experiment, data, window):
    """
    """
    message = ""
    try:
        selected_name = data['outputs']['source_spectrum'][0]
        meggie_spectrum = experiment.active_subject.source_spectrum[selected_name]

        message += "Name: "+ str(meggie_spectrum.name) + "\n\n"
    except Exception as exc:
        message = ""
    return message

