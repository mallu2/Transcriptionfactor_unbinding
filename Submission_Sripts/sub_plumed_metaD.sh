#!/bin/bash
#SBATCH -n 32
#SBATCH -t 160:00:00
#SBATCH -c 4 #CPU cores per rank -- 32 ranks
#SBATCH -J metaDNA
#SBATCH -A 

# Start with a clean environment
module purge

# Substitute with your required GMX module
#module load GROMACS/2019.6-PLUMED-nsc1-gcc-7.3.0-bare

module load GROMACS/2021.3-PLUMED-nsc1-gcc-9.3.0-bare

# Load your python environment
#source activate myownmdtraj

# Set the number of OpenMP threads equal to whatever
# you set your SBATCH '-c' option to, using a default of 1
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:=1}

# this is for 200 ns of production

# Make sure the MPI launch works for the number of OpenMP threads
# requested and let GROMACS match and pin these as it deems fit.

mpprun --pass="--map-by socket:pe=${OMP_NUM_THREADS}" \
gmx_mpi mdrun \
-plumed plumed_run.dat \
-nsteps 100000000 \
-ntomp ${OMP_NUM_THREADS} \
-pin on \
-npme 4 #-append -cpi state.cpt
