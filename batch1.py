import pickle
from FAmodel import Forest
from FAmodel import sumendos
from FAmodel import sumdecomps
from FAagents import Tree, Wood, Fungus
import numpy as np
import matplotlib.pyplot as plt
import thomasprocess as tp


endo_runs = {}
decomp_runs = {}
for i in [ a/10 for a in range(2,22,2) ]: ## levels of variable
    endo_list = []
    decomp_list = []
    for j in range(100): ## number of simulations per level of parameter
        losced = Forest(endophytism = False, ##settings for model
                        endodisp=1, 
                        decompdisp=i, ## parameter of interest
                        )
        for j in range(30): losced.step() ## number of steps before ending the model
        ## data into lists
        endo_list.append(losced.datacollector.get_model_vars_dataframe().Endophytes)
        decomp_list.append(losced.datacollector.get_model_vars_dataframe().Decomposers) 
    endo_runs[i] = endo_list
    decomp_runs[i] = decomp_list

## seems like a we want a dictionary, with a key for each level of dispersal, 
## containing a list of the resulting dataframes. 

pickle.dump(endo_runs, open('endo_runs.p', 'wb'))
pickle.dump(decomp_runs, open('decomp_runs.p', 'wb'))


