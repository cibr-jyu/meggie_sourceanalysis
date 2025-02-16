import os
import shutil


class Coregistration(object):
    """Takes care of params and files related to a coregistration."""

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
    def path(self):
        return self._path

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        self._params = params

    @property
    def subjects_dir(self):
        return os.path.join(self._path, self._name, "subjects")

    @property
    def trans_path(self):
        # should probably have a better way..
        subject_name = os.path.basename(os.path.dirname(self._path))
        return os.path.join(self._path, self._name, subject_name + "-trans.fif")

    def save_content(self):
        """Placeholder for saving content. Currently all files are created
        into folders already."""
        pass

    def delete_content(self):
        """Deletes the files from fs."""
        if os.path.exists(self._path):
            shutil.rmtree(self._path)
