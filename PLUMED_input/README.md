This folder contains the input files for metadynamics simulations using PLUMED.
PLUMED_files contains input files for 5 different simulations: 4 are for the simulations with a starting structure that contains the specific sequence OSymL and 1 for simulations starting from a complex containing the non-specific sequence NOD. The 4 different simulations for each sequence use different collective variables in the metadynamics simulations. 

1. specific : specific protein-DNA contacts
-------------------------------------------
CMAP collective variable is used and the contacts are defined by selecting protein side chains that are known to contribute to specific binding to base edges of the DNA. The pairs for contacts are then defined as the closest contacts between those protein side chains and the base edges.

2. hinge_contacts : specific protein-DNA contacts and hinge-helix contacts
--------------------------------------------------------------------------
CMAP collective variable is used and the same specific contacts between protein and DNA as in the previous run are included. Additionally contacts between the residues in the hinge helices are included to dissociate their interaction interface.
3. alphaRMSD: specific protein-DNA and hinge-helix contacts as well as the helicity of the hinge helix
------------------------------------------------------------------------------------------------------
The same CMAP collective variable as in 2. is used. Additionally the ALPHARMSD collective variable for the two hinge regions is included. As there are 7 residues in each of the 2 helices and a stretch of 6 residues can be counted as one helix, dependent of the backbone torsional angles, the ALPHARMSD is 4 when both helices are completely structured and 0 when the are not.
4. DNA_bending : specific protein-DNA and hinge-helix contacts, hinge ALPHARMSD and DNA bending angle
-----------------------------------------------------------------------------------------------------
The same CMAP and ALPHARMSD collective variables as in 3. are used. Additionally the DNA bending at the center of the operator is included as a 3. CV.    


The gromacs topologies can be prepared like the ones for the NMR simulations using the the structures in Starting_Structures plus DNA restraints in DNA_restraints, the protocol in GMX_2023.sh, the force field parameters from amber99sbws_md_K.ff and the  input files from GROMACS_input. The simulations were run with GROMACS 2021.2 patched with PLUMED.
Simulations have been run for 100000000 MD steps using 32 cores and 4 ranks per CPU core. They have been launched using mpprun and 4 ranks have been dedicated to long-range PME interactions.   
 
