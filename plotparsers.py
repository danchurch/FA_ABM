## some parsing functions to take the outputs from our sweeps
## needs to be a dictionary of levels 

import numpy as np

## for single-species experiments
def pldata1(runs,lvl,sims=50):
    means = []
    stds = []
    for j in range(sims): ## for all 50 time steps
        datime = [] ## decomposer abundances for a particular timestep, all 100 runs
        for i in runs[lvl]: ## for all the 100 sims from disp=1
            datime.append(i.Decomp_subs[j]) ## add this simulation's decomps total to the list
         ## calculate 
        means.append(np.mean(datime))
        stds.append(np.std(datime))
    updev = np.array(means) + np.array(stds) ## add error
    updev[updev < 0] = 0 ## get rid of negatives
    downdev = np.array(means) - np.array(stds) ## sub error
    downdev[downdev < 0] = 0 ## get rid of negatives
    pltdata = {'means':means,'updev':updev, 'downdev':downdev}
    return(pltdata)

## for two-species, competition-type experiments
def pldata2(runs,lvl,sims=50):
    decomp_means = []
    decomp_stds = []
    endo_means = []
    endo_stds = []
    for j in range(sims): ## for all 50 time steps
        datime = [] ## decomposer abundances for a particular timestep, all 100 runs
        eatime = [] ## endophyte abundances for a particular timestep, all 100 runs
        for i in runs[lvl]: ## for all the 100 sims from disp=j
            datime.append(i.Decomp_subs[j]) ## add this simulation's decomps total to the list
            eatime.append(i.Endo_subs[j]) ## add this simulation's endophyte total to the list
         ## create the time series of means and stdevs:
        decomp_means.append(np.mean(datime))
        decomp_stds.append(np.std(datime))
        endo_means.append(np.mean(eatime))
        endo_stds.append(np.std(eatime))
    ## decomp error zone:
    decomp_updev = np.array(decomp_means) + np.array(decomp_stds) ## add error
    decomp_updev[decomp_updev < 0] = 0 ## get rid of negatives
    decomp_downdev = np.array(decomp_means) - np.array(decomp_stds) ## sub error
    decomp_downdev[decomp_downdev < 0] = 0 ## get rid of negatives
    ## decomp error zone:
    endo_updev = np.array(endo_means) + np.array(endo_stds) ## add error
    endo_updev[endo_updev < 0] = 0 ## get rid of negatives
    endo_downdev = np.array(endo_means) - np.array(endo_stds) ## sub error
    endo_downdev[endo_downdev < 0] = 0 ## get rid of negatives
    ## store it in a dictionary:
    pltdata = {'decomp_means':decomp_means,
                'decomp_updev':decomp_updev,
                'decomp_downdev':decomp_downdev,
                'endo_means':endo_means,
                'endo_updev':endo_updev,
                'endo_downdev':endo_downdev,
              }
    return(pltdata)

