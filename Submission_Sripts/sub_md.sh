#!/bin/bash -l

#SBATCH -A 
#SBATCH -N 1
#SBATCH -n 32
#SBATCH -t 7-00:00:00
#SBATCH -J md_1EFA_Rest

#load modules
module load GROMACS/2019.6-nsc1-gcc-7.3.0-bare

#Production 
gmx_mpi mdrun -ntomp 32 -s md_NMR.tpr -x md_NMR.xtc -e md_NMR.edr -c md_NMR.gro -cpo md_NMR.cpt -g md_NMR.log
