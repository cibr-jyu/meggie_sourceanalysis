import os
import logging


class Inverse(object):
    """
    """
    def __init__(self, name, inv_directory, params, content=None):
        self._name = name
        self._content = content
        self._path = inv_directory
        self._params = params

    @property
    def content(self):
        if self._content:
            return self._content

        # read from file
        # ...

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

    def delete_content(self):
        """
        """

