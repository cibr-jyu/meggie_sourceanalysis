"""Contains implementation for coregistration info"""

from meggie.mainwindow.dynamic import InfoAction


class Info(InfoAction):
    """Fills up coregistration info box"""

    def run(self, params={}):

        message = ""
        try:
            selected_name = self.data["outputs"]["coregistration"][0]
            meggie_coreg = self.experiment.active_subject.coregistration[selected_name]

            message += "Name: " + meggie_coreg.name + "\n\n"
        except Exception:
            message = ""

        return message
