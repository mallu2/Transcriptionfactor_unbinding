These are scripts that were used to analyse trajectories from MD. They have all been used in the jupyter notebooks that produced plots from the data. They read GROMACS and PLUMED output files into pandas DataFrames and some do further processing such as calculating histograms for replicas and averaging them for plotting with seaborn.

plotting_gmx.py
---------------
contains functions that plot RMSDs for different protein regions and hydrogen bonds between the protein and the DNA as well as within the protein.

analysis_of_CVs.py
------------------
contains functions that read data from different simulations, calculated and plots average histograms mean and 68% confidence interval.  

analysis_of_CVs_NMR.py
----------------------
s.o. but specifically for plots of NMR simulations.

