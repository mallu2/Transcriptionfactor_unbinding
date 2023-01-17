#!/bin/bash -l

#SBATCH -A 
#SBATCH -N 1
#SBATCH -n 16
#SBATCH -t 10:00:00
#SBATCH -J nvt

#load modules
module load GROMACS

#run GROMACS parallel
mpprun gmx_mpi mdrun -v -deffnm nvt
