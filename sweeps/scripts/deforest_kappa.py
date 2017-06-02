import pickle
from FAmodel import Forest
from FAmodel import sumendos
from FAmodel import sumdecomps
from FAagents import Tree, Wood, Fungus
import numpy as np
import matplotlib.pyplot as plt
import thomasprocess as tp


kaps = [ 0.03,0.02,0.01,0.005,0.002,0.001 ]
runs = {}
for i in kaps: ## levels of variable
    run_list = []
    for j in range(100): ## number of simulations per level of parameter
        losced = Forest(endophytism = True, ##settings for model
                        ws = 30,
                        woodfreq = 1,
                        newwood = 4,
                        endodisp = 1, 
                        decompdisp=5, 
                        kappa = i, ## variable of interest
                        sigma = 3.0, 
                        mu = 2.2, 
                        )
        for j in range(50): losced.step() ## number of steps before ending the model
        ## data into lists
        run_list.append(losced.datacollector.get_model_vars_dataframe())
    runs[i] = run_list
    
pickle.dump(runs, open('deforest_kappa.p', 'wb'))

