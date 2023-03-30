#!/bin/bash -l

#SBATCH -A snic2021-3-8
#SBATCH -N 1
#SBATCH -n 16
#SBATCH -t 00:20:00
#SBATCH -J pluAna

module load PLUMED/2.7.1-nsc1-gcc-9.3.0-bare
rm bck.0.CVs 
plumed driver --plumed plumed_print.dat --mf_pdb 1osl_C52V_GMX_new_numbering.pdb --pdb 1osl_C52V_GMX_new_numbering_f1.pdb
