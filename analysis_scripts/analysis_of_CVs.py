import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
sys.path.append("/home/malinlu/elflab/Projects/MD_lacI/") #for the RMSD plotting function
from gmx_tool import plotting_gmx

def read_CVs(folder):
    """Read the PLUMED output file produced by plumed_print.dat into a pandas DataFrame.
    
    Parameters
    ----------
    folder : str
        path to folder with the data.
        
    Returns
    -------
    CVs : pandas DataFrame
        The data of the CVs file from metadynamics as a pandas DataFrame for plotting.
    """
    
    CVs = pd.read_csv(folder + "CVs", sep='\s+', skiprows=1, \
    names=['Time (ps)', 'Contacts', 'Formed Helices', 'DNA bent (rad)', 'Hinge Distance (nm)',\
           'Distance Hinge A to DNA (nm)',\
           'Distance Hinge B to DNA (nm)', 'Specific Contacts', 'Hinge Helix Contacts'])
    
    cmap_sum = pd.read_csv(folder + "distances", sep='\s+', skiprows=1, \
    names=['Time (ps)', 'dist1', 'dist2', 'dist3', 'dist4', 'dist5', 'dist6', 'dist7', \
           'dist8', 'dist9', 'dist10', 'dist11', 'dist12', 'dist13', 'dist14', 'dist15', \
           'dist16', 'dist17', 'dist18', 'dist19', 'dist20', 'dist21'])
    
    CVs["DNA Bent (deg)"] = (-1)*(((CVs['DNA bent (rad)']/(np.pi))*180)-180)

    return(CVs)

def CVs_replicas(folder, N_replica, path_ana = False ):
    """Summarizes the CVs data from different replica.
    
    Parameters
    ----------
    folder : str
        path to folder with the data.
    N_replica : int
        number of replicas to analyse
    path_ana : str (default is False if it doesn't need to be specified)
        if the file is in a subfolder
        
    Returns
    -------
    CVs : pandas DataFrame
        The data of the CVs file from metadynamics as a pandas DataFrame for plotting.
    """
    CVs = []
    for i in np.arange(1,N_replica+1,1):
        if path_ana:
            Cv_N = read_CVs(folder+'{}/'.format(i)+path_ana)
        else:
            Cv_N = read_CVs(folder+'{}/'.format(i))
    
        Cv_N["Time (ns)"] = Cv_N["Time (ps)"]/1000
        Cv_N["Replica"] = [i for x in range(len(Cv_N))]
        Cv_N["Hinge DNA\nDistance (nm)"] = (Cv_N["Distance Hinge A to DNA (nm)"]+Cv_N["Distance Hinge A to DNA (nm)"])/2

        CVs.append(Cv_N)
    CVs_all = pd.concat([x for x in CVs])
    return(CVs_all)

def plot_hbonds(folder, N_replica, path_ana = False):
    """Extract hbonds record produced by gmx_mpi 
    
    Parameters
    ----------
    folder : str
        path to folder with the data.
    N_replica : int
        number of replicas to analyse
    path_ana : str (default is False if it doesn't need to be specified)
        if the file is in a subfolder
        
    Returns
    -------
    hbonds : pandas DataFrame
        The data from the gromacs hbond analysis as a pandas DataFrame for plotting.
    """
    
    if path_ana:
        hbonds = plotting_gmx.plot_hb_num(folder + "1/" + path_ana + "ana/" )[1]
    else:
        hbonds = plotting_gmx.plot_hb_num(folder + "1/ana/" )[1]
    
    hbonds['Replica'] = [1 for x in range(len(hbonds))]
    hbonds['Time (ns)'] = hbonds['Time (ps)']/1000
    hbonds.rename(columns={"h-bonds":"Protein-DNA H-Bonds"}, inplace=True)
    for i in np.arange(2,N_replica+1,1):
        if path_ana:
            hbonds_n = plotting_gmx.plot_hb_num(folder + "{}/".format(i) + path_ana + "ana/" )[1]
        else:
            hbonds_n = plotting_gmx.plot_hb_num(folder+'{}/ana/'.format(i))[1]
        hbonds_n['Time (ns)'] = hbonds_n['Time (ps)']/1000
        hbonds_n['Replica'] = [i for x in range(len(hbonds_n))]
        hbonds_n.rename(columns={"h-bonds":"Protein-DNA H-Bonds"}, inplace=True)
        hbonds = hbonds.append(hbonds_n)
    plt.show()
    return(hbonds)

def get_mean_hist(data, feature, bindef, frames=None):    
    """This gets the histogram for each collective variable.
    
    Parameters
    ----------
    data : pandas DataFrame
        contains all the data that can be assessed by the column name.
    feature : str
        feature that data should be histogrammed for.
    bindef : numpy array
        array with bins used for creating the histogram.
    frames : int
	specify which frames should be used in the analysis. They will be bigger than what is specified with frames.
        
    Returns
    -------
    hist_rep : numpy array
        histogram for a value split into a certain bin range."""
        
    hist_rep = []
    for i in np.array(data["Replica"][0]):
        if frames:
            hist, y  = np.histogram(data[(data["Replica"] == i) & (data["Time (ps)"] >= frames)][feature],bins = bindef, density = True)
        else:
            hist, y  = np.histogram(data[(data["Replica"] == i)][feature],\
                 bins = bindef, density = True)
        hist_rep.append(hist)
        
    return(hist_rep)

def Write_Probability_Data_Frame(CVs, CV, bin_range, plot_t="bar",figsize=(2.2,1.8), figure_path=None):
    """
    Write the probabilities for a feature along with the bins of NMR and unbiased simulations to a dataframe and plot.
    
    Parameters
    ----------
    CVs : pandas DataFrame
        dataframe with all the data
    CV : str
        feature that data should be histogrammed for.
    bin_range : numpy array
        array with bins used for creating the histogram.
    plot_t : str
        style of the plot: bar: bar chart with error bars. line = line plot with shading for error (error=SEM).
    hbonds_ : bool (default:False)
        specifies if you are analysing hbonds if True, otherwise will analyse CVs.
    figsize : list, default=(2.2,1.8)
	size of the figure.
    figure_path : str, default=None
	path to where the figure is saved.
	
    Returns
    -------
    df : pandas DataFrame
        Contains the bins and the corresponding probabilities for the specified feature and for 3 simulations:
        NMR restraint with NOD as well as OSymL sequences and unbiased simulations.
        
    Line or barplots with probabilities compaing the NMR sampling with NOD and OSymL sequences to unbiased simulations. 
    The errors are Standard errors of the mean (68 % confidence intervals).
    If paths are specified the plots can be saved as image files.
    """

    ub = get_mean_hist(CVs[CVs["Simulation"] == "Unbiased , OSymL"], CV, bin_range)
    SymL = get_mean_hist(CVs[CVs["Simulation"] == "MetaD, OSymL"], CV, bin_range)
    NMR = get_mean_hist(CVs[CVs["Simulation"] == "NMR, OSymL"], CV, bin_range, frames=250000)
    
    df = pd.DataFrame({"Simulation":\
                  ["Unbiased, OSymL" for x in range(len(ub))]*(len(bin_range)-1)+\
                                       ["MetaD, OSymL" for x in range(len(SymL))]*(len(bin_range)-1)+\
                                       ["NMR, OSymL" for x in range(len(NMR))]*(len(bin_range)-1), "Probability":\
                  [x for y in ub for x in y]+\
                                       [x for y in SymL for x in y]+\
                       [x for y in NMR for x in y],\
                 CV: [x for y in [bin_range[1:] for x in range(13)] for x in y]})
    
    ax = sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 1}) #font size is 10
    
    fig, axs = plt.subplots(figsize=figsize)

    if plot_t=="bar":
        sns.barplot(data = df, y="Probability", x=CV, hue = "Simulation",\
                hue_order=["MetaD, OSymL","Unbiased, OSymL","NMR, OSymL"], ci=68, errwidth=1, capsize=.15, \
                palette=["purple", "cyan", "brown"], errcolor=".5", edgecolor=".5")
        plt.xlim(-1,bin_range[-1])
        plt.ylim(-0.1,1.1)

        if (CV=="Specific Contacts") :
            plt.xticks(np.arange(0,bin_range[-1],5),np.arange(1,bin_range[-1]+1,5))
        else:
            plt.xticks(np.arange(0,bin_range[-1],1),np.arange(1,bin_range[-1]+1,1))
           
    if plot_t=="line":
        df.drop(columns=CV)
        df[CV]=[x for y in [bin_range[:-1] for x in range(13)] for x in y]
        sns.lineplot(data = df, y="Probability", x=CV, hue = "Simulation",\
                hue_order=["MetaD, OSymL","Unbiased, OSymL", "NMR, OSymL"], ci=68, \
                palette=["purple", "cyan", "brown"], style="Simulation")

        if (CV=="Specific Contacts") :
            plt.xticks(np.arange(0,bin_range[-1],5),np.arange(0,bin_range[-1],5))
        elif (CV=="DNA Bent (deg)") or (CV=="Protein-DNA H-Bonds"):
            plt.xticks(np.arange(0,bin_range[-1],10),np.arange(0,bin_range[-1],10))
        else:
            plt.xticks(np.arange(0,bin_range[-1]+1,1),np.arange(0,bin_range[-1]+1,1))
        plt.xlim(bin_range[0]-1/15,bin_range[-1]+1/15)

    plt.legend([],[])
    if figure_path:
        plt.tight_layout()
        plt.savefig(figure_path+'_{}'.format(CV), dpi=300)
    plt.show()
    
    return(df)
