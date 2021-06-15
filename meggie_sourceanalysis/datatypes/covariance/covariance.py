import os
import logging

from mne.cov import write_cov
from mne.cov import read_cov


class Covariance(object):
    """
    """
    def __init__(self, name, cov_directory, params, content=None):
        self._name = name
        self._content = content
        self._path = os.path.join(cov_directory, name + '-cov.fif')
        self._params = params

    @property
    def content(self):
        if self._content:
            return self._content

        self._content = read_cov(self._path) 
        return self._content

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        self._params = params

    def save_content(self):
        """
        """
        try:
            write_cov(self._path, self.content)
        except Exception as exc:
            logging.getLogger('ui_logger').exception('')
            raise IOError('Writing covariance failed')

    def delete_content(self):
        """
        """
        os.remove(self._path)

