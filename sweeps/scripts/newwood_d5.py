import pickle
from FAmodel import Forest
from FAmodel import sumendos
from FAmodel import sumdecomps
from FAagents import Tree, Wood, Fungus
import numpy as np
import matplotlib.pyplot as plt
import thomasprocess as tp

######## sweeping wood deposition rates ################

decomp_runs = {}
for i in [ i for i in range(1,13,1) ]: ## levels of variable
    #endo_list = []
    decomp_list = []
    for j in range(100): ## number of simulations per level of parameter
        losced = Forest(endophytism = False, ##settings for model
                        newwood=i, ## parameter of interest
                        decompdisp=5, ## hold fungal dispersal here
                        endodisp=0, ## no blue fungi
                        )
        for j in range(50): losced.step() ## number of steps before ending the model
        ## data into lists
        #endo_list.append(losced.datacollector.get_model_vars_dataframe().Endophytes)
        decomp_list.append(losced.datacollector.get_model_vars_dataframe().Decomposers)
    decomp_runs[i] = decomp_list

pickle.dump(decomp_runs, open('newwood_d5.p','wb'))
