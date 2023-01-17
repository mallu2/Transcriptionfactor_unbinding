#!/bin/bash -l

#SBATCH -A 
#SBATCH -N 1
#SBATCH -n 16
#SBATCH -t 3:00:00
#SBATCH -J npt


#load modules
module load GROMACS

#run gromacs parallel
mpprun gmx_mpi mdrun -v -deffnm npt
