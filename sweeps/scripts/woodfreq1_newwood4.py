############ d=5, newwood = 4, woodfreq = 1 #########

import pickle
from FAmodel import Forest
from FAmodel import sumendos
from FAmodel import sumdecomps
from FAagents import Tree, Wood, Fungus
import numpy as np
import matplotlib.pyplot as plt
import thomasprocess as tp

decomp_list = []
for j in range(100): ## number of simulations per level of parameter
    losced = Forest(endophytism = False, ##settings for model
                    newwood=4, ## wood depo
                    woodfreq=1, ## parameter of interest
                    decompdisp=5, ## hold fungal dispersal here
                    endodisp=0, ## no blue fungi
                    )
    for j in range(50): losced.step() ## number of steps before ending the model
    ## data into lists
    #endo_list.append(losced.datacollector.get_model_vars_dataframe().Endophytes)
    decomp_list.append(losced.datacollector.get_model_vars_dataframe().Decomposers)

pickle.dump(decomp_list, open('/home/daniel/Documents/ABM/FA/sweeps/results/woodfreq1_newwood4.p','wb'))

