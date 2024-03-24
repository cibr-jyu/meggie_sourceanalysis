import os


from mne.minimum_norm.inverse import write_inverse_operator
from mne.minimum_norm.inverse import read_inverse_operator


class Inverse(object):
    """ """

    def __init__(self, name, inv_directory, params, content=None):
        self._name = name
        self._content = content
        self._path = os.path.join(inv_directory, name + "-inv.fif")
        self._params = params

    @property
    def content(self):
        if self._content:
            return self._content

        self._content = read_inverse_operator(self._path)
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
        """ """
        try:
            write_inverse_operator(self._path, self.content)
        except Exception:
            raise IOError(
                "Writing inverse failed. Please ensure that the "
                "entire experiment folder has write permissions."
            )

    def delete_content(self):
        """ """
        os.remove(self._path)
