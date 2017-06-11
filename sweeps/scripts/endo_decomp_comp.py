## a function to make a sweep

################################

import pickle
from FAmodel import Forest
from FAmodel import sumendos
from FAmodel import sumdecomps
from FAagents import Tree, Wood, Fungus
import numpy as np
import matplotlib.pyplot as plt
import thomasprocess as tp

lvls = [ 0.5, 1, 2, 4, 6, 8 ]
with open('updates_endo_decomp_comp.txt', 'a') as upd:
    runs = {}
    for i in lvls: ## levels of variable
        run_list = [] 
        upd.write('starting level: %s \n' %i)
        for j in range(100): ## number of simulations per level of parameter
            losced = Forest( 
                    endophytism = True, 
                    ws = 30, 
                    endodisp=i, # variable of interest
                    decompdisp=8, 
                    leafdisp = 4, 
                    leaffall = 1, 
                    numdecomp=1, 
                    numendo=1,   
                    endoloss=0.05,   
                    newwood = 15, 
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

pickle.dump(runs, open('endo_decomp_comp.p', 'wb'))

###############

## 17216 labcomp PID


############

## okay, those programs are taking forever. 

## I assume this is my inefficient coding. There
## are a lot of agents in these models.

## but I don't want to be afraid of having lots
## of agents. This is the computer age, for god's 
## sake. Why else are we destroying our climate and
## our mental health if we can't get a simple
## model to work.

## Can I figure out multiprocessing?

## for the moment, let's break up the sweeps 
## into smaller scripts, for the aciss sh file 
## to initiate, one by one. At least we won't 
## lose 

## we can also use bitty's comp to run these.

## so for the endodisp sweep:

## endodisp sweep 7:

import pickle
from FAmodel import Forest
from FAmodel import sumendos
from FAmodel import sumdecomps
from FAagents import Tree, Wood, Fungus
import numpy as np
import matplotlib.pyplot as plt
import thomasprocess as tp


lvls = list(range(7,8,1)) ## reduced

with open('updates_endo_disp_7.txt', 'a') as upd:
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

pickle.dump(runs, open('endo_disp_7.p', 'wb'))

