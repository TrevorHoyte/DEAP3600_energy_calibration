# DEAP3600_energy_calibration
Calibrates the Energy in the DEAP-3600 detector using AmBe runs


This code is devoted to recreating Trevor's Energy correction / time dependet B parameter.

Please read the STR: https://www.overleaf.com/project/63ed02c58eb68364065b602a
or the Analysis Notes FIrst before proceding: https://www.snolab.ca/deap/private/TWiki/bin/view/DEAP3/AnalysisNotex664

-To start your going to need to put all the AmBe runs in to one directory. see the Skim directory for help

GetB directory 

1)next your going to want to run multipeak.py
multipeak will set the basis of the entire work it fits gaussians to the qPE spectrum of ambe runs and saves the infromation in a root file and a pdf

2)abc_making.py this file will now use the peak information generated from multipeak.py to find parameter B that best fits the data.

3)in order to get B parameters for evry single phys run we know have to group up the Ambe runs in 5 day windows and then linearly interpolate 
the B parameter for all phys runs. this uses get_-bestruns_avg.py and then make_every_abc.py

Validation DIrectory
here are the files to validate your work

bparameter_time.py is used to plot a temporal plot of how B parameter changes over time

cr_peak_trevor_corr.py compute the location of the Cr peak using either  the time depemndent b parameter.
uncertainty_calc.py uses the output of crPeak_trevor_corr.py to plot the Cr peak residuals for the fits

Phys validation simply validates the energy correction using phys data
draw_data.py compares differnt phys runs after a trevorcorr
