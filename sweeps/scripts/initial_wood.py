import pickle
from FAmodel import Forest
from FAmodel import sumendos
from FAmodel import sumdecomps
from FAagents import Tree, Wood, Fungus
import numpy as np
import matplotlib.pyplot as plt
import thomasprocess as tp

with open('init_wood_upd.txt', 'a') as upd:
    lvls = list(range(5,65,5))
    runs = {}
    for i in lvls: ## levels of variable
        run_list = []
        upd.write('starting level: %s \n' %i)
        for j in range(100): ## number of simulations per level of parameter
            losced = Forest(
                endophytism = True, ## allow endophyte life style in model run
                ws = i, ## initial num of wood
                endodisp=1, ## dispersal of endos
                decompdisp=8, ## dispersal of decomps
                leafdisp = 4, ## how well do leaves disperse
                leaffall = 1, ## how frequently do leaves disperse
                numdecomp=1, ## initial number of decomposers
                numendo=1,   ## initial number of endos
                endoloss=0.05,   ## rate of loss of endophyte infect per step
                newwood = 6, ## total energy added in new logs each step
                woodfreq = 1, ## how often to put new logs onto the landscape
                width = 100, ## grid dimensions, only one (squares only)
                kappa = 0.03, ## average rate of parent tree clusters per unit distance
                sigma = 3.0, ## variance of child tree clusters, +/- spread of child clusters
                mu = 2.2, ## average rate of child tree clusters per unit distance
                            )
            for j in range(50): losced.step() ## number of steps before ending the model
            run_list.append(losced.datacollector.get_model_vars_dataframe())
        upd.write('completed level: %s \n' %i)
            ## data into lists
        runs[i] = run_list

pickle.dump(runs, open('initial_wood.p', 'wb'))

