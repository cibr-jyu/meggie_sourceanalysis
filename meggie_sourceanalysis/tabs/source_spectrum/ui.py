import logging 

import numpy as np

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.names import next_available_name

from meggie.utilities.formats import format_float

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

    logging.getLogger('ui_logger').info('Deleted source spectrum: ' + selected_name)
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
        logging.getLogger('ui_logger').info('Computing.. can take a while.')
        create_source_spectrum(subject, spectrum_name, params, intervals, inv_name,
                               do_meanwhile=window.update_ui)

    dialog = PowerSpectrumDialog(experiment, window, default_name, handler=handler)
    dialog.show()


def plot_spectrum(experiment, data, window):
    """ 
    """
    selected_name = data['outputs']['source_spectrum'][0]
    meggie_spectrum = experiment.active_subject.source_spectrum[selected_name]

    stcs = meggie_spectrum.content

    subjects_dir = meggie_spectrum.params['subjects_dir']

    for key, stc in stcs.items():
        logging.getLogger('ui_logger').info('Plotting ' + str(key))

        # scale to avoid overflows
        stc_copy = stc.copy()
        stc_copy.data = stc_copy.data / np.max(np.abs(stc_copy.data))
        stc_copy.plot(time_label=("%0.2f Hz"), hemi='both', subjects_dir=subjects_dir)

def info(experiment, data, window):
    """
    """
    message = ""
    try:
        selected_name = data['outputs']['source_spectrum'][0]
        meggie_spectrum = experiment.active_subject.source_spectrum[selected_name]

        params = meggie_spectrum.params

        message += "Name: "+ meggie_spectrum.name + "\n\n"

        if 'fmin' in params and 'fmax' in params:
            message += 'Frequencies: {0}Hz - {1}Hz\n'.format(format_float(params['fmin']),
                                                             format_float(params['fmax']))

        if 'nfft' in params:
            message += 'Window length (samples): {0}\n'.format(params['nfft'])

        if 'overlap' in params:
            message += 'Overlap (samples): {0}\n'.format(params['overlap'])

        if 'intervals' in params:
            message += '\nIntervals: \n'
            for key, ivals in params['intervals'].items():
                message += 'Condition ' + str(key) + ': '
                message += ', '.join(['({0}s - {1}s)'.format(format_float(ival[0]), format_float(ival[1]))
                                      for ival in ivals])
                message += '\n'

        if 'groups' in params:
            for key, names in params['groups'].items():
                message += '\nGroup ' + str(key) + ': \n'
                for name in names:
                    message += name + '\n'

    except Exception as exc:
        message = ""
    return message

