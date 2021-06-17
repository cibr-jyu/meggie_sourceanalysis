import os
import logging


class Coregistration(object):
    """
    """
    def __init__(self, name, path, params, content=None):
        self._name = name
        self._content = content
        self._path = path
        self._params = params

    @property
    def content(self):
        if self._content:
            return self._content

        self._content = None

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
            pass
        except Exception as exc:
            logging.getLogger('ui_logger').exception('')
            raise IOError('Writing covariance failed')

    def delete_content(self):
        """
        """
        pass

