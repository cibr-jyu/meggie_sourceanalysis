import os
import shutil
import logging


class Coregistration(object):
    """ Takes care of params and files related to a coregistration.
    """
    def __init__(self, name, path, params):
        self._name = name
        self._path = path
        self._params = params

    @property
    def content(self):
        return None

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
        """ Placeholder for saving content. Currently all files are created
        into folders already. """
        pass

    def delete_content(self):
        """ Deletes the files from fs.
        """
        if os.path.exists(self._path):
            shutil.rmtree(self._path)


