"""Contains implementation for inverse info"""

import os

from meggie.mainwindow.dynamic import InfoAction


class Info(InfoAction):
    """Fills up inverse info box"""

    def run(self, params={}):

        message = ""
        try:
            selected_name = self.data["outputs"]["inverse"][0]
            meggie_inv = self.experiment.active_subject.inverse[selected_name]

            inv = meggie_inv.content

            message += "Name: " + str(meggie_inv.name) + "\n\n"

            message += (
                "Based on trans: " + os.path.basename(inv["info"]["mri_file"]) + "\n\n"
            )

            message += "Source space: \n"
            message += "LH: " + str(len(inv["src"][0]["vertno"])) + " vertices" + "\n"
            message += "RH: " + str(len(inv["src"][1]["vertno"])) + " vertices" + "\n"

            message += "\n"

            message += "lambda2: " + str(meggie_inv.params["lambda2"]) + "\n"
            message += "Method: " + str(meggie_inv.params["method"]) + "\n"

        except Exception:
            message = ""
        return message
