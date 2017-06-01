import pickle
from FAmodel import Forest
from FAmodel import sumendos
from FAmodel import sumdecomps
from FAagents import Tree, Wood, Fungus
import numpy as np
import matplotlib.pyplot as plt
import thomasprocess as tp


runs = {}
for i in [ a for a in range(1,8,1) ]: ## levels of variable
    run_list = []
    for j in range(100): ## number of simulations per level of parameter
        losced = Forest(endophytism = True, ##settings for model
                        ws = 30,
                        woodfreq = 1,
                        newwood = 4,
                        endodisp = i, ## parameter of interest
                        decompdisp=5, 
                        )
        for j in range(50): losced.step() ## number of steps before ending the model
        ## data into lists
        run_list.append(losced.datacollector.get_model_vars_dataframe())
    runs[i] = run_list
    
pickle.dump(runs, open('first_endo_comp.p', 'wb'))


