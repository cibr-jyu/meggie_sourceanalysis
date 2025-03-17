# Meggie Source Analysis Plugin (Proof of Concept)

This is a proof of concept plugin for source analysis in Meggie. It's in development and not ready for general use. Feedback and contributions are welcome.

## Current Status

### Implemented
- [x] Coregistration with MNE coreg for trans files
- [x] Ad hoc covariance calculation (diagonal only)
- [x] Inverse solutions using coregistrations and covariances
- [x] Source power spectral density (PSD) computation and visualization

These features form a basic pipeline for continuous source-space data analysis.

### To Do
- [ ] Complete pipeline for continuous data
- [ ] Add SourceEpochs and SourceEvoked actions and datatypes
- [ ] Add SourceEpochs and SourceTFR for time-frequency analysis
- [ ] Improve covariance estimation methods

## Installation:

1. Activate the existing meggie environment
3. Install: python -m pip install meggie\_sourceanalysis

If everything went fine, meggie should now recognize the plugin and you can enable it from the settings.

## Note

This plugin is a work in progress, and we're aware of its limitations. If you have any suggestions or would like to help, please let us know.
