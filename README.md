# Pipelines, actions and datatypes for source analysis in Meggie (work in progress)

## Currently implemented:
* Actions and datatypes for coregistrations, covariances, inverses and source spectrums
* Coregistration tab uses mne coreg to create trans files.
* Covariance tab has currently only ad hoc cov (diagonal).
* Inverse tab combines coregistrations and covariances to create inverses (via fwd).
* Source spectrums can be created with compute\_source\_psd and plotted with plot\_source\_estimates
* All in all, almost full pipeline for continuous source-space data analysis.

## TODO:
* Finishing the pipeline for continuous data analysis.
* Evoked (SourceEpochs and SourceEvoked actions and datatypes needed)
* TFR (SourceEpochs and SourceTFR actions and datatypes needed)
* Covariance estimation

## Installation:

1. Activate the meggie environment
1. Install: python -m pip install meggie\_sourceanalysis

## Usage:

If everything went fine, meggie should now recognize the plugin and you can enable it from the settings.

## Contributions:

Help very much appreciated.
