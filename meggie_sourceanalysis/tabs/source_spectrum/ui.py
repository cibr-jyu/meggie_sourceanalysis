from meggie.utilities.messaging import messagebox


def delete(experiment, data, window):
    """ 
    """
    message = 'Delete for {}!'.format(experiment.active_subject.name)
    messagebox(window, message)


def create(experiment, data, window):
    """
    """
    message = 'Create for {}!'.format(experiment.active_subject.name)
    messagebox(window, message)


def plot_spectrum(experiment, data, window):
    """ 
    """
    message = 'Plot spectrum for {}!'.format(experiment.active_subject.name)
    messagebox(window, message)


def info(experiment, data, window):
    """
    """

