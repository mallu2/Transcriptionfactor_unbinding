#!/bin/bash -l
#SBATCH -A 
#SBATCH -N 1
#SBATCH -n 1 
#SBATCH -t 0:20:00
#SBATCH -J ana


#get the concat trajectory, 10 offset
echo "24" |gmx_mpi trjconv -f traj_comp.xtc -s topol.tpr -o md_compact_vac.xtc -pbc mol -ur compact -n protein_DNA.ndx -skip 10
echo "24" |gmx_mpi trjconv -f traj_comp.xtc -s topol.tpr -o md_compact_vac.pdb -pbc mol -ur compact -n protein_DNA.ndx -dump 0
echo "0" |gmx_mpi trjconv -f md_compact_vac.xtc -s md_compact_vac.pdb -o md_compact_vac_no_jump.xtc -pbc nojump
echo "1 0" |gmx_mpi trjconv -f md_compact_vac_no_jump.xtc -s topol_vac.tpr -o md_compact_vac_no_jump_fit.xtc -fit rot+trans

##RMSD and RMSF
echo "0 1" |gmx_mpi rms -f md_compact_vac_no_jump.xtc -s topol.tpr -o DBD_rmsd.xvg -n core_DBD_combined.ndx
echo "0 0" |gmx_mpi rms -f md_compact_vac_no_jump.xtc -s topol.tpr -o core_rmsd.xvg -n core_DBD_combined.ndx
echo "0 2" |gmx_mpi rms -f md_compact_vac_no_jump.xtc -s topol.tpr -o DNA_rmsd.xvg -n core_DBD_combined.ndx
echo "1" |gmx_mpi rmsf -f md_compact_vac_no_jump.xtc -s topol.tpr -o Flux_Protein.xvg -n Protein.ndx -res
echo "12" |gmx_mpi rmsf -f md_compact_vac_no_jump.xtc -s topol.tpr -o Flux_DNA.xvg -n DNA.ndx -res

#analyse h-bonds
echo "1 1" |gmx_mpi hbond -f md_compact_vac_no_jump.xtc -s topol.tpr -num hbnum_Pro-Pro.xvg
echo "1 12" |gmx_mpi hbond -f md_compact_vac_no_jump.xtc -s topol.tpr -num hbnum_DNA-Pro.xvg

#rm \#*
mkdir ana
#rm ana/*
mv *xvg ana
