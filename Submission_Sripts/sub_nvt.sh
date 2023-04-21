#!/bin/bash -l

#SBATCH -A 
#SBATCH -N 1
#SBATCH -n 16
#SBATCH -t 10:00:00
#SBATCH -J nvt

#load modules
module load GROMACS/2019.6-nsc1-gcc-7.3.0-bare

#run GROMACS parallel
mpprun gmx_mpi mdrun -v -deffnm nvt
