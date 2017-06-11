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

## instantiate our parser:
parser = argparse.ArgumentParser()

losced = Forest()

## model parameters:
parser.add_argument("-no_endophytism", action='store_false', required=False)
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
parser.add_argument("-fileout", required=True)


## get our commandline arguments into the environment
args = parser.parse_args()

run_list = [] 
for j in range(args.sims): ## number of simulations per level of parameter
#for j in range(5): ## testing_________

    losced = Forest(endophytism = args.no_endophytism)
    ## the initial wood settings have to be put in place at the instantiation of the model:
    if args.ws: losced = Forest(endophytism = args.no_endophytism, ws = args.ws)
    if args.endodisp: losced.endodisp = args.endodisp
    if args.decompdisp: losced.decompdisp = args.decompdisp 
    if args.leafdisp: losced.leafdisp = args.leafdisp 
    if args.leaffall: losced.leaffall = args.leaffall 
    if args.numdecomp: losced.numdecomp = args.numdecomp 
    if args.numendo: losced.numendo = args.numendo 
    if args.endoloss: losced.endoloss = args.endoloss 
    if args.newwood: losced.newwood = args.newwood 
    if args.woodfreq: losced.woodfreq = args.woodfreq 
    if args.width: losced.width = args.width 
    ## the thomas process settings also have to be put in place at the instantiation of the model:
    if args.kappa: losced = Forest(endophytism = args.no_endophytism, kappa = args.kappa)
    if args.sigma: losced = Forest(endophytism = args.no_endophytism, sigma = args.sigma)
    if args.mu: losced = Forest(endophytism = args.no_endophytism, mu = args.mu)
    #for k in range(50): losced.step() ## number of steps before ending the model
    for k in range(2): losced.step() ## testing_________
    run_list.append(losced.datacollector.get_model_vars_dataframe())
    ## data into lists

pickle.dump(run_list, open('%s.p' %args.fileout, 'wb'))


