import pickle
from FAmodel import Forest
from FAmodel import sumendos
from FAmodel import sumdecomps
from FAagents import Tree, Wood, Fungus
import numpy as np
import matplotlib.pyplot as plt
import thomasprocess as tp

blue_runs = {}
red_runs = {}
for i in [ a for a in range(1,11,1) ]: ## levels of variable
    blue_list = []
    red_list = []
    for j in range(100): ## number of simulations per level of parameter
        losced = Forest(endophytism = False, ##settings for model
                        ws = 30,
                        woodfreq = 1,
                        newwood = 4,
                        endodisp = i, ## parameter of interest
                        decompdisp=5, 
                        )
        for j in range(50): losced.step() ## number of steps before ending the model
        ## data into lists
        blue_list.append(losced.datacollector.get_model_vars_dataframe().Endophytes)
        red_list.append(losced.datacollector.get_model_vars_dataframe().Decomposers)
    blue_runs[i] = blue_list
    red_runs[i] = red_list


pickle.dump(blue_runs, open('compet_onlydecomp_blue.p', 'wb'))
pickle.dump(red_runs, open('compet_onlydecomp_red.p', 'wb'))

###################
