"""Contains implementation for covariance info"""

from meggie.mainwindow.dynamic import InfoAction


class Info(InfoAction):
    """Fills up covariance info box"""

    def run(self, params={}):

        message = ""
        try:
            selected_name = self.data["outputs"]["covariance"][0]
            meggie_cov = self.experiment.active_subject.covariance[selected_name]

            message += "Name: " + meggie_cov.name + "\n\n"
        except Exception:
            message = ""

        return message
