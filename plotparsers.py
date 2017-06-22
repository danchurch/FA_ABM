## some parsing functions to take the outputs from our sweeps
## needs to be a dictionary of levels 

import numpy as np


def pldata(runs,lvl,sims=50):
    decomp_means = []
    decomp_stds = []
    endo_means = []
    endo_stds = []
    inf_trees_means = []
    inf_trees_stds = []
    despo_means = []
    despo_stds = []
    espo_means = []
    espo_stds = []

    for j in range(sims): ## for all 50 time steps
        datime = [] ## decomposer abundances for a particular timestep, all 100 runs
        eatime = [] ## endophyte abundances for a particular timestep, all 100 runs
        inf_trees = [] ## num of infected trees for a particular timestep, all 100 runs
        despo = [] ## num of infected trees for a particular timestep, all 100 runs
        espo = [] ## num of infected trees for a particular timestep, all 100 runs
        for i in runs[lvl]: ## for all the 100 sims from disp=j
            datime.append(i.Decomp_subs[j]) ## add this simulation's decomps total to the list
            eatime.append(i.Endo_subs[j]) ## add this simulation's endophyte total to the list
            inf_trees.append(i.Infected_trees[j]) ## add this simulation's endophyte total to the list
            despo.append(i.decompspor_count[j]) ## add this simulation's endophyte total to the list
            espo.append(i.endospor_count[j]) ## add this simulation's endophyte total to the list
         ## create the time series of means and stdevs:
        decomp_means.append(np.mean(datime))
        decomp_stds.append(np.std(datime))

        endo_means.append(np.mean(eatime))
        endo_stds.append(np.std(eatime))

        inf_trees_means.append(np.mean(inf_trees))
        inf_trees_stds.append(np.std(inf_trees))

        despo_means.append(np.mean(despo))
        despo_stds.append(np.std(despo))

        espo_means.append(np.mean(espo))
        espo_stds.append(np.std(espo))

    ## decomp error zone:
    decomp_updev = np.array(decomp_means) + np.array(decomp_stds) ## add error
    decomp_updev[decomp_updev < 0] = 0 ## get rid of negatives
    decomp_downdev = np.array(decomp_means) - np.array(decomp_stds) ## sub error
    decomp_downdev[decomp_downdev < 0] = 0 ## get rid of negatives

    ## endo error zone:
    endo_updev = np.array(endo_means) + np.array(endo_stds) ## add error
    endo_updev[endo_updev < 0] = 0 ## get rid of negatives
    endo_downdev = np.array(endo_means) - np.array(endo_stds) ## sub error
    endo_downdev[endo_downdev < 0] = 0 ## get rid of negatives

    ## inf_trees error zone:
    inf_trees_updev = np.array(inf_trees_means) + np.array(inf_trees_stds) ## add error
    inf_trees_updev[inf_trees_updev < 0] = 0 ## get rid of negatives
    inf_trees_downdev = np.array(inf_trees_means) - np.array(inf_trees_stds) ## sub error
    inf_trees_downdev[inf_trees_downdev < 0] = 0 ## get rid of negatives

    ## despo error zone:
    despo_updev = np.array(despo_means) + np.array(despo_stds) ## add error
    despo_updev[despo_updev < 0] = 0 ## get rid of negatives
    despo_downdev = np.array(despo_means) - np.array(despo_stds) ## sub error
    despo_downdev[despo_downdev < 0] = 0 ## get rid of negatives

    ## espo error zone:
    espo_updev = np.array(espo_means) + np.array(espo_stds) ## add error
    espo_updev[espo_updev < 0] = 0 ## get rid of negatives
    espo_downdev = np.array(espo_means) - np.array(espo_stds) ## sub error
    espo_downdev[espo_downdev < 0] = 0 ## get rid of negatives

    ## store it in a dictionary:
    pltdata = {'decomp_means':decomp_means,
                'decomp_updev':decomp_updev,
                'decomp_downdev':decomp_downdev,
                'endo_means':endo_means,
                'endo_updev':endo_updev,
                'endo_downdev':endo_downdev,

                'inf_trees_means':inf_trees_means,
                'inf_trees_updev':inf_trees_updev,
                'inf_trees_downdev':inf_trees_downdev,

                'despo_means':despo_means,
                'despo_updev':despo_updev,
                'despo_downdev':despo_downdev,

                'espo_means':espo_means,
                'espo_updev':espo_updev,
                'espo_downdev':espo_downdev,
              }
    return(pltdata)

