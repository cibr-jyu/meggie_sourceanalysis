"""Contains implementation for source spectrum info"""

from meggie.utilities.formats import format_float

from meggie.mainwindow.dynamic import InfoAction


class Info(InfoAction):
    """Fills up source spectrum info box"""

    def run(self, params={}):
        message = ""
        try:
            selected_name = self.data["outputs"]["source_spectrum"][0]
            meggie_spectrum = self.experiment.active_subject.source_spectrum[
                selected_name
            ]

            params = meggie_spectrum.params

            message += "Name: " + meggie_spectrum.name + "\n\n"

            if "fmin" in params and "fmax" in params:
                message += "Frequencies: {0}Hz - {1}Hz\n".format(
                    format_float(params["fmin"]), format_float(params["fmax"])
                )

            if "nfft" in params:
                message += "Window length (samples): {0}\n".format(params["nfft"])

            if "overlap" in params:
                message += "Overlap (samples): {0}\n".format(params["overlap"])

            if "intervals" in params:
                interval_parts = [
                    f"Condition {key}: "
                    + ", ".join(
                        f"({format_float(ival[0])}s - {format_float(ival[1])}s)"
                        for ival in ivals
                    )
                    for key, ivals in params["intervals"].items()
                ]
                message += "\nIntervals: \n" + "\n".join(interval_parts) + "\n"

            if "groups" in params:
                for key, names in params["groups"].items():
                    message += "\nGroup " + str(key) + ": \n"
                    for name in names:
                        message += name + "\n"

        except Exception:
            message = ""
        return message
