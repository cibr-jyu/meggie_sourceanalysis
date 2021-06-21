# Tabs and datatypes for source analysis in Meggie (work in progress)

## Currently implemented:
* Tabs and datatypes for coregistrations, covariances, inverses and source spectrums
* Coregistration tab uses mne coreg to create trans files.
* Covariance tab has currently only ad hoc cov (diagonal).
* Inverse tab combines coregistrations and covariances to create inverses (via fwd).
* Source spectrums can be created with compute\_source\_psd and plotted with plot\_source\_estimates
* All in all, almost full pipeline for continuous source-space data analysis.

## TODO:
* Permutation tests and data saving for spectrums
* Evoked (SourceEpochs and SourceEvoked datatypes and tabs needed)
* TFR (SourceEpochs and SourceTFR datatypes and tabs needed)
* Covariance estimation

## Installation:

Currently only via setuptools i.e:

1. Clone the repository
2. cd to root directory
3. Run: python setup.py install

Depends on meggie>=1.1.1.

## Contributions

Help appreciated!
