from meggie.utilities.messaging import messagebox
from meggie.utilities.names import next_available_name

from meggie.utilities.dialogs.powerSpectrumDialogMain import PowerSpectrumDialog

from meggie_sourceanalysis.tabs.source_spectrum.controller.source_spectrum import create_source_spectrum


def delete(experiment, data, window):
    """ 
    """

def create(experiment, data, window):
    """ Uses spectrum creation dialog from core meggie
    """
    default_name = next_available_name(
        experiment.active_subject.source_spectrum.keys(), 'Spectrum')
     
    try:
        inv_name = data['inputs']['inverse'][0]
    except Exception as exc:
        messagebox('Inverse need to be selected for computing source spectrums')
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

