#!/bin/bash -l

#SBATCH -A SNIC2022-3-26
#SBATCH -n 1
#SBATCH -t 00:30:00
#SBATCH -J ana



# Start with a clean environment
module purge

# Substitute with your required GMX module
module load GROMACS/2019.6-nsc1-gcc-7.3.0-bare

#RMSD and RMSF
echo "2 2" | gmx_mpi rms -f 1osl_C52V_GMX_new_numbering.pdb -s 1osl_C52V_GMX_new_numbering_f1.pdb -o DBD_rmsd.xvg
echo "2 1" |gmx_mpi rms -f 1osl_C52V_GMX_new_numbering.pdb -s 1osl_C52V_GMX_new_numbering_f1.pdb -o DNA_rmsd.xvg
echo "2" |gmx_mpi rmsf -f 1osl_C52V_GMX_new_numbering.pdb -s 1osl_C52V_GMX_new_numbering_f1.pdb -o Flux_Protein.xvg -res
echo "1" |gmx_mpi rmsf -f 1osl_C52V_GMX_new_numbering.pdb -s 1osl_C52V_GMX_new_numbering_f1.pdb -o Flux_DNA.xvg -res


#analyse h-bonds
echo "1 2" |gmx_mpi hbond -f 1osl_C52V_GMX_new_numbering.xtc -s 1osl_C52V_GMX_nn_f1.tpr -num hbnum_DNA-Pro.xvg
echo "2 2" |gmx_mpi hbond -f 1osl_C52V_GMX_new_numbering.xtc -s 1osl_C52V_GMX_nn_f1.tpr -num hbnum_Pro-Pro.xvg

rm \#*
mkdir ana
mv *xvg ana
mv dr* ana
