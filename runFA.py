################################

## let's make a script that can run our sims with
## arguments from the command line:

import pickle
from FAmodel import Forest
from FAmodel import sumendos
from FAmodel import sumdecomps
from FAagents import Tree, Wood, Fungus
import numpy as np
import matplotlib.pyplot as plt
import thomasprocess as tp
import argparse
import datetime
import logging


## instantiate our parser:
parser = argparse.ArgumentParser()

## model parameters:
parser.add_argument("-endophytism", type=bool, required=False)
parser.add_argument("-ws", type=float, required=False)
parser.add_argument("-endodisp", type=float, required=False)
parser.add_argument("-decompdisp", type=float, required=False)
parser.add_argument("-leafdisp", type=float, required=False)
parser.add_argument("-leaffall", type=float, required=False)
parser.add_argument("-numdecomp", type=float, required=False)
parser.add_argument("-numendo", type=float, required=False)
parser.add_argument("-endoloss", type=float, required=False)
parser.add_argument("-newwood", type=float, required=False)
parser.add_argument("-woodfreq", type=float, required=False)
parser.add_argument("-width", type=float, required=False)
parser.add_argument("-kappa", type=float, required=False)
parser.add_argument("-sigma", type=float, required=False)
parser.add_argument("-mu", type=float, required=False)
## set number of simulations:
parser.add_argument("-sims", type=int, required=True)
## output pickle file name:
parser.add_argument("-fileout", required=False)


## get our commandline arguments into the environment
args = parser.parse_args()

## set our filename
if args.fileout: ## if one was set by user
    fileout = args.fileout
else: ## if not, timestamp
    fileout = 'run.' + str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.') 

## set log
logging.basicConfig(filename=fileout + '.log',level=logging.INFO)

logging.info('start %s' %datetime.datetime.now().time().isoformat())
logging.info('usersets %s' %args)

run_list = [] 
for j in range(args.sims): ## number of simulations per level of parameter

    ## make an empty landscape, enable/disable endophytism
    losced = Forest(
                    nuke = True
                    )

    ## set user-defined changes to defaults of model:

    if args.endophytism is not None: losced.endophytism = args.endophytism
    if args.ws is not None: losced.ws = args.ws
    if args.endodisp is not None: losced.endodisp = args.endodisp
    if args.decompdisp is not None: losced.decompdisp = args.decompdisp 
    if args.leafdisp is not None: losced.leafdisp = args.leafdisp 
    if args.leaffall is not None: losced.leaffall = args.leaffall 
    if args.numdecomp is not None: losced.numdecomp = args.numdecomp 
    if args.numendo is not None: losced.numendo = args.numendo 
    if args.endoloss is not None: losced.endoloss = args.endoloss 
    if args.newwood is not None: losced.newwood = args.newwood 
    if args.woodfreq is not None: losced.woodfreq = args.woodfreq 
    if args.width is not None: losced.width = args.width 
    if args.kappa is not None: losced.kappa = args.kappa 
    if args.sigma is not None: losced.sigma = args.sigma
    if args.mu is not None: losced.mu = args.mu

    ## now add in initial agents, with new model settings:
    losced.make_trees()
    for i in range(losced.nwood): losced.add_wood() ## no make_woods method
    losced.make_fungi()

    for k in range(50):  ## number of steps before ending the model
    #for k in range(2): ## test, just two steps 
        losced.step() 
        logging.info('run %s step %s' %(j,k)) ## what step?
        fun=sum([ type(i)==Fungus for i in losced.schedule.agents ]) ## number of fungi
        logging.info('num of fungi %s' %fun)
    run_list.append(losced.datacollector.get_model_vars_dataframe())


picklefile = fileout + ".p"
pickle.dump(run_list, open(picklefile, 'wb'))

logging.info('finish %s' %datetime.datetime.now().time().isoformat())
