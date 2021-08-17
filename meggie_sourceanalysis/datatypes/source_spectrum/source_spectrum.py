import os
import logging

import mne


class SourceSpectrum(object):
    """
    """
    def __init__(self, name, spectrum_directory, params, content=None):
        self._name = name
        self._path = spectrum_directory
        self._params = params

        self._content = {}
        if content is not None:
            self._content = content

    @property
    def content(self):
        if self._content:
            return self._content

        for key in self._params['conditions']:
            path = os.path.join(self._path, self._name + '_' + key)
            self._content[key] = mne.read_source_estimate(path, 
                subject=self._params['fs_subject'])

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
        try:
            for key, psd_stc in self._content.items():
                psd_stc.save(
                    os.path.join(self._path, self._name + '_' + str(key)))
        except Exception as exc:
            raise IOError("Writing spectrums failed. Please ensure that the "
                          "entire experiment folder has write permissions.")

    def delete_content(self):
        deleted_paths = []
        for key, _ in self.content.items():
            deleted_paths.append(os.path.join(self._path, self._name + '_' + 
                                                          str(key) + '-lh.stc'))
            deleted_paths.append(os.path.join(self._path, self._name + '_' + 
                                                          str(key) + '-rh.stc'))
        for path in deleted_paths:
            os.remove(path)

