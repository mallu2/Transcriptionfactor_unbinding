#!/bin/bash -l
#SBATCH -A
#SBATCH -n 16
#SBATCH -J min
#SBATCH --time=00:50:00


module load GROMACS/2019.6-nsc1-gcc-7.3.0-bare

mpprun gmx_mpi mdrun -v -deffnm min
