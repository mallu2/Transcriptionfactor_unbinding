import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns

def plot_ana_rmsd(ana_f):
    """ Plot the root mean square deviation of atomic positions for core, DNA binding domains and DNA.

    Parameters
    ----------
    ana_f: str
	the folder with the .xvg files.
    """

    DNA = pd.read_csv( ana_f + "DNA_rmsd.xvg" , sep='\s+', skiprows=18, names=["Time (ps)", "RMSD (nm)"])
    DBD = pd.read_csv( ana_f + "DBD_rmsd.xvg" , sep='\s+', skiprows=18, names=["Time (ps)", "RMSD (nm)"])
    core = pd.read_csv( ana_f + "core_rmsd.xvg" , sep='\s+', skiprows=18, names=["Time (ps)", "RMSD (nm)"])
    DNA['domain'] = ['DNA' for x in range ( len(DNA) )]
    DBD['domain'] = ['DBD' for x in range ( len(DBD) ) ]
    core['domain'] = ['core' for x in range ( len(core) ) ]
    
    rmsd = pd.concat([DBD, core, DNA])
    sns.lineplot ( data=rmsd, x = "Time (ps)", y = "RMSD (nm)", hue = "domain" )
    return(rmsd)

def plot_ana_rmsd_apo(ana_f):
    """ Plot the root mean square deviation of atomic positions for core, DNA binding domains and DNA.

    Parameters
    ----------
    ana_f: str
	the folder with the .xvg files.
    """

    DBD = pd.read_csv( ana_f + "DBD_rmsd.xvg" , sep='\s+', skiprows=18, names=["MD steps", "RMSD (nm)"])
    core = pd.read_csv( ana_f + "core_rmsd.xvg" , sep='\s+', skiprows=18, names=["MD steps", "RMSD (nm)"])
    DBD['domain'] = ['DBD' for x in range ( len(DBD) ) ]
    core['domain'] = ['core' for x in range ( len(core) ) ]
    
    rmsd = pd.concat([DBD, core])
    rmsd["Time (ps)"] = rmsd["MD steps"].copy()*0.002
    sns.lineplot ( data=rmsd, x = "Time (ps)", y = "RMSD (nm)", hue = "domain" )
    return(rmsd)

def plot_ana_rmsd_2(ana_f):
    """ Plot the root mean square deviation of atomic positions for core, DNA binding domains and DNA.

    Parameters
    ----------
    ana_f: str
	the folder with the .xvg files.
    """

    DNA = pd.read_csv( ana_f + "DNA_rmsd_2.xvg" , sep='\s+', skiprows=18, names=["Time (ps)", "RMSD (nm)"])
    DBD = pd.read_csv( ana_f + "DBD_rmsd_2.xvg" , sep='\s+', skiprows=18, names=["Time (ps)", "RMSD (nm)"])
    core = pd.read_csv( ana_f + "core_rmsd_2.xvg" , sep='\s+', skiprows=18, names=["Time (ps)", "RMSD (nm)"])
    DNA['domain'] = ['DNA' for x in range ( len(DNA) )]
    DBD['domain'] = ['DBD' for x in range ( len(DBD) ) ]
    core['domain'] = ['core' for x in range ( len(core) ) ]
    
    rmsd = pd.concat([DBD, core, DNA])
    sns.lineplot ( data=rmsd, x = "Time (ps)", y = "RMSD (nm)", hue = "domain" )
    return(rmsd)

def plot_ana_rmsf(ana_f):
    """ Plot the root mean square fluction of atomic positions for proteins and DNA.

    Parameters
    ----------
    ana_f: str
	the folder with the .xvg files.
    """
    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True)
    DNA = pd.read_csv( ana_f + "Flux_DNA.xvg" , sep='\s+', skiprows=17, names=["Residue", "RMSF (nm)"])
    protein = pd.read_csv( ana_f + "Flux_Protein.xvg" , sep='\s+', skiprows=17, names=["Residue", "RMSF (nm)"])
  
    ax1.plot(protein['Residue'], protein["RMSF (nm)"])
    ax1.set_title('protein')
    ax1.set_ylabel("RMSF (nm)")
    ax1.set_xlabel("Residue ID")
    
    ax2.plot(DNA['Residue'], DNA["RMSF (nm)"] )
    ax2.set_title('DNA')
    ax2.set_ylabel("RMSF (nm)")
    ax2.set_xlabel("Residue ID")
    
    fig.tight_layout()
    return(protein,DNA)

def plot_hb_num(ana_f):
    """ Plot the number of protein-protein and protein-DNA bonds along the trajectory.

    Parameters
    ----------
    ana_f: str
	the folder with the .xvg files.
    """
    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharex=True)
    DNA = pd.read_csv( ana_f + "hbnum_DNA-Pro.xvg" , sep='\s+', skiprows=25, names=["Time (ps)", "h-bonds", "pairs within 0.35 nm"])
    protein = pd.read_csv( ana_f + "hbnum_Pro-Pro.xvg" , sep='\s+', skiprows=25, names=["Time (ps)", "h-bonds", "pairs within 0.35 nm"])

    ax1.plot(protein['Time (ps)'], protein["h-bonds"])
    ax1.set_title('protein')
    ax1.set_ylabel("N (h-bonds)")
    ax1.set_xlabel("Time (ps)")

    ax2.plot(DNA['Time (ps)'], DNA["h-bonds"] )
    ax2.set_title('protein-DNA')
    ax2.set_ylabel("N (h-bonds)")
    ax2.set_xlabel("Time (ps)")
    
    fig.tight_layout()
    return(protein,DNA)	
