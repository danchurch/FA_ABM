import pickle
from FAmodel import Forest
from FAmodel import sumendos
from FAmodel import sumdecomps
from FAagents import Tree, Wood, Fungus
import numpy as np
import matplotlib.pyplot as plt
import thomasprocess as tp

lvls = list(range(1,11,1))
with open('updates_endo_disp.txt', 'a') as upd:
    runs = {}
    for i in lvls: ## levels of variable
        run_list = [] 
        upd.write('starting level: %s \n' %i)
        for j in range(100): ## number of simulations per level of parameter
            losced = Forest( 
                    endophytism = True, ## Turn on endos
                    ws = 30,
                    endodisp=i, ## variable of interest
                    decompdisp=0, ## Turn off EC- fungi
                    leafdisp = 4,
                    leaffall = 1, 
                    numdecomp=1,
                    numendo=1,
                    endoloss=0.05,
                    newwood = 6, ## low rate of wood deposition
                    woodfreq = 1,
                    width = 100,
                    kappa = 0.03, ## dense forest
                    sigma = 3.0,
                    mu = 2.2,
                            )
            for j in range(50): losced.step() ## number of steps before ending the model
            run_list.append(losced.datacollector.get_model_vars_dataframe())
        upd.write('completed level: %s \n' %i)
            ## data into lists
        runs[i] = run_list

pickle.dump(runs, open('endo_disp.p', 'wb'))

