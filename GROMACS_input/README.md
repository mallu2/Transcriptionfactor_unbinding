Input files with parameters for preparation and running of the molecular dynamics simulations with GROMACS. 

ions.mdp places ions using steepest descent optimization.

minim.mdp minimizes the energy of the structure using steepest descent minimizationi.

nvt.mdp contains the parameters for a simulation in the NVT ensemble where the protein is kept fixed. The system run at 310 K.
npt.mdp eqeuilibrates the system to T=310 K and P=1 bar.
The equilibration steps use the V-scale thermostat und the Berendsen barostat with respective time constants of 0.1 and 2 ps. 

md_prod_NMR.mdp was used for the NMR restraint simulations.
md_prod.mdp was used for the unbiased and the metadynamics simulations.

