###############################################

## what next?

## don't need to redo initial wood abundances,
## I think we get the message there. 

## so let's redo the wood deposition trials


import pickle
from FAmodel import Forest
from FAmodel import sumendos
from FAmodel import sumdecomps
from FAagents import Tree, Wood, Fungus
import numpy as np
import matplotlib.pyplot as plt
import thomasprocess as tp

with open('updates_newwood.txt', 'a') as upd:
    lvls = [ a for a in range(1,10,1) ]
    runs = {}
    for i in lvls: ## levels of variable
        run_list = []
        upd.write('starting level: %s \n' %i)
        for j in range(100): ## number of simulations per level of parameter
            losced = Forest(
                    endophytism = False, ## Turn off endos
                    ws = 30,
                    endodisp=0, ## Turn off endos
                    decompdisp=8, 
                    leafdisp = 4,
                    leaffall = 1,
                    numdecomp=1,
                    numendo=1,
                    endoloss=0.05,
                    newwood = i, ## variable of interest
                    woodfreq = 1,
                    width = 100,
                    kappa = 0.03,
                    sigma = 3.0,
                    mu = 2.2,
                            )
            for j in range(50): losced.step() ## number of steps before ending the model
            run_list.append(losced.datacollector.get_model_vars_dataframe())
        upd.write('completed level: %s \n' %i)
            ## data into lists
        runs[i] = run_list

pickle.dump(runs, open('newwood_sweep.p', 'wb'))

