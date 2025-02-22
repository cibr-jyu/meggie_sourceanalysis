"""Contains implementation for delete source spectrum"""

from meggie.utilities.messaging import exc_messagebox

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class DeleteSpectrum(Action):
    """Deletes source spectrum items"""

    def run(self, params={}):

        subject = self.experiment.active_subject

        try:
            selected_name = self.data["outputs"]["source_spectrum"][0]
        except IndexError:
            return

        try:
            self.handler(subject, {"name": selected_name})
        except Exception as exc:
            exc_messagebox(self.window, exc)
            return

        self.window.initialize_ui()

    @subject_action
    def handler(self, subject, params):
        subject.remove(params["name"], "source_spectrum")
        self.experiment.save_experiment_settings()
