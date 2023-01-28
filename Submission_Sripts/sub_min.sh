#!/bin/bash -l
#SBATCH -A SNIC2021-3-8
#SBATCH -n 16
#SBATCH -J min
#SBATCH --time=00:50:00
#SBATCH --mail-type=fail
#SBATCH --mail-user=malin.luking@icm.uu.se

#module load GROMACS/2021.3-PLUMED-nsc1-gcc-9.3.0-bare

module load GROMACS/2019.6-nsc1-gcc-7.3.0-bare

mpprun gmx_mpi mdrun -v -deffnm min
