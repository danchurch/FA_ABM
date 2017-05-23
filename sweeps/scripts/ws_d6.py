###################################################

## if it works, do the above with decomp disp=6, too?

decomp_runs = {}
for i in [ i for i in range(20,80,10) ]: ## levels of variable
    #endo_list = []
    decomp_list = []
    for j in range(100): ## number of simulations per level of parameter
        losced = Forest(endophytism = False, ##settings for model
                        ws=i, ## parameter of interest
                        decompdisp=6, ## hold fungal dispersal here
                        endodisp=0, ## no blue fungi
                        )
        for j in range(50): losced.step() ## number of steps before ending the model
        ## data into lists
        #endo_list.append(losced.datacollector.get_model_vars_dataframe().Endophytes)
        decomp_list.append(losced.datacollector.get_model_vars_dataframe().Decomposers)
    decomp_runs[i] = decomp_list

pickle.dump(decomp_runs, open('ws_d6.p','wb'))


