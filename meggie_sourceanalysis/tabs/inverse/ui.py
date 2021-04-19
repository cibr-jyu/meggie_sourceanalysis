from meggie.utilities.messaging import messagebox


def import_inv(experiment, data, window):
    """ 
    """
    message = 'Import for {}!'.format(experiment.active_subject.name)
    messagebox(window, message)


def delete(experiment, data, window):
    """ 
    """
    message = 'Delete for {}!'.format(experiment.active_subject.name)
    messagebox(window, message)


def info(experiment, data, window):
    """
    """

