from mesa import Agent, Model
from mesa.time import RandomActivation
import random
import numpy as np
import thomasprocess as tp
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from FAagents import Tree, Wood, Fungus
from mesa.datacollection import DataCollector

##### reporter functions #######

## this is the number of endophyte-competent fungi that have found a log to rot
def sumendos(model): 
    isendo = [ type(i)==Fungus and i.endocomp for i in model.schedule.agents ]
    sumendos = sum(isendo)
    return(sumendos)

## this is the number of endophyte-INcompetent fungi that have found a log to rot
def sumdecomps(model):
    isdecomp = [ type(i)==Fungus and not i.endocomp for i in model.schedule.agents ]
    sumdecomps = sum(isdecomp)
    return(sumdecomps)

## both of the above are a little misleading. Two fungal agents of the same 
## species can be sharing a log, I built this in to reflect the possibility
## that heavy dispersal of spores from nearby may cause quicker rot, allows the
## a fungus to infect a substrate at different points. But not that informative
## as a statistic for our purposes. 

## so here are the number of substrates that EC+ and EC- fungi occupy in 
## total, no extra points for having multiple infections on that piece of 
## wood:

def Endo_subs(model):
    endocomps = 0
    for cell in model.grid.coord_iter():
        cell_content = list(cell[0])
        if any([ type(i) == Fungus for i in cell_content ]):
            isfung  = np.array([ type(i) == Fungus for i in cell_content ])
            fung = np.array(cell_content)[isfung]
            if any( i.endocomp for i in fung ): endocomps += 1
    return(endocomps)

def Decomp_subs(model):
    decomps = 0
    for cell in model.grid.coord_iter():
        cell_content = list(cell[0])
        if any([ type(i) == Fungus for i in cell_content ]):
            isfung  = np.array([ type(i) == Fungus for i in cell_content ])
            fung = np.array(cell_content)[isfung]
            if any( not i.endocomp for i in fung ): decomps += 1
    return(decomps)

## track the number of endophyte-infected trees at every step:
def bluetrees(model): 
    return(len([ i for i in model.schedule.agents if type(i)==Tree and i.infection==True ]))

## track the sporulations of EC- fungi:

def decompspor_count(model):
    return(model.decompspor)

def endospor_count(model):
    return(model.endospor)

###### model #######
class Forest (Model): 
    def __init__ (self,  
                endophytism = True, ## allow endophyte life style in model run
                ws = 30, ## initial num of wood
                endodisp=2.0, ## dispersal of endos
                decompdisp=10.0, ## dispersal of decomps
                leafdisp = 4.0, ## how well do leaves disperse
                leaffall = 1, ## how frequently do leaves disperse
                numdecomp=1, ## initial number of decomposers
                numendo=1,   ## initial number of endos
                endoloss=0.05,   ## rate of loss of endophyte infect per step
                newwood = 15, ## total energy added in new logs each step
                woodfreq = 1, ## how often to put new logs onto the landscape 
                width = 100, ## grid dimensions, only one (squares only)
                kappa = 0.03, ## average rate of parent tree clusters per unit distance 
                sigma = 3.0, ## variance of child tree clusters, +/- spread of child clusters
                mu = 2.2, ## average rate of child tree clusters per unit distance 
                nuke = False, ## make landscape, but no agents
                ): 

        self.endophytism = endophytism 
        self.nwood = ws 
        self.endodisp = endodisp 
        self.decompdisp = decompdisp 
        self.leafdisp = leafdisp
        self.leaffall = leaffall 
        self.numdecomp = numdecomp 
        self.numendo = numendo 
        self.endoloss = endoloss 
        self.newwood = newwood 
        self.woodfreq = woodfreq
        self.schedule = RandomActivation(self) 
        self.grid = MultiGrid(width, width, torus = True)
        self.running = True
        self.width = width 
        self.kappa = kappa
        self.sigma = sigma
        self.mu = mu
        self.decompspor = 0 ## sporulation events this turn
        self.endospor = 0 ## sporulation events this turn
        self.datacollector = DataCollector(
            model_reporters={
                "Endophytes": sumendos,
                "Endo_subs": Endo_subs,
                "Decomposers": sumdecomps,
                "Decomp_subs": Decomp_subs,
                "Infected_trees": bluetrees,
                "decompspor_count": decompspor_count,
                "endospor_count": endospor_count,
                })

        ## make initial agents:
        if not nuke: ## if not a nuclear holocaust where life is devoid
            self.make_trees()
            for i in range(self.nwood): self.add_wood() ## no make_woods method
            self.make_fungi()

    def make_trees(self):
        ## let's use our thomas process module
        tname = 1

        positions = tp.makepos(tp.ThomasPP(kappa = self.kappa, 
                                sigma=self.sigma, 
                                mu=self.mu, 
                                Dx=self.grid.width-1))
        for i in positions:
                try:
                    tree = Tree(tname, self, i, 
                                disp = self.leafdisp, 
                                leaffall = self.leaffall,
                                endoloss = self.endoloss,
                                infection = False)
                    self.schedule.add(tree) 
                    self.grid.place_agent(tree, i)
                    tname += 1
                except IndexError:
                    print ("Tree out-of-bounds, ipos=",i,"grid dim=", self.grid.width, self.grid.height)

    ## add initial wood to landscape
    def add_wood(self): 
        wname = len(self.getall(Wood)) + 1 
        x = random.randrange(self.grid.width)
        y = random.randrange(self.grid.height)
        pos = (x, y)
        ## wood already present? then just add to the pile
        if any([ type(i)==Wood for i in self.grid.get_cell_list_contents(pos) ]):
            for i in self.grid.get_cell_list_contents(pos):
                if type(i)==Wood: 
                    i.energy += random.randrange(self.newwood) ## 
        else:
            wood = Wood(wname, self, pos, energy = random.randrange(self.newwood)+1) ## 
            self.grid.place_agent(wood, (x,y))
            self.schedule.add(wood)
            wname += 1 

    ## non-initial, step addition of wood
    def cwd(self): 
        cwdlist = [round(random.randrange(self.newwood))+1] ## our first log of the step, at least 1 
        while sum(cwdlist) < round(self.newwood*.9)-1 : ## until we get at 90% of our assigned cwd...
            newlog=round(random.randrange(self.newwood-sum(cwdlist)))+1 ## new log, at least 1 kg
            cwdlist.append(newlog) ## put newlog on the list, until newwood reached)
        wname = len(self.getall(Wood)) + 1 
        for i in cwdlist:
            self.add_wood()

    def make_fungi(self):
        fname = len(self.getall(Fungus)) + 1 

        ## decomposers first:
        decomps=0
        while decomps < self.numdecomp:
            pos = self.findsubstrate(Wood)
            if any([ type(i)==Fungus for i in self.grid.get_cell_list_contents(pos) ]):
                pass 
            else:
                fungus = Fungus(fname, self, pos, energy=10, endocomp=False, disp = self.decompdisp)
                self.schedule.add(fungus) 
                self.grid.place_agent(fungus, pos)
                fname += 1; decomps += 1

        ## then endophytes:
        endos=0
        while endos < self.numendo:
            pos = self.findsubstrate(Wood)
            if any([ type(i)==Fungus for i in self.grid.get_cell_list_contents(pos) ]):
                pass
            else:
                fungus = Fungus(fname, self, pos, energy=10, endocomp=True, disp = self.endodisp)
                self.schedule.add(fungus) 
                self.grid.place_agent(fungus, pos)
                fname += 1; endos += 1


    def findsubstrate (self, substrate):
        Subs = self.getall(substrate)
        try:
            somestick = (random.choice(Subs).pos) ## pick from these, return position
            return(somestick) ## pick from these, return position
        except IndexError:
            print("no substrates")
            pass



    def getall(self, typeof):
        if not any([ type(i)==typeof for i in self.schedule.agents ]):
            return([])
        else:
            istype = np.array([ type(i)==typeof for i in self.schedule.agents ])
            ags = np.array(self.schedule.agents)
            return list(ags[istype])

    def step(self): 
        if self.schedule.time % self.woodfreq ==  self.woodfreq - 1: ##  = delay from start
            self.cwd() ## add wood
        self.schedule.step() ## agents do their thing
        self.datacollector.collect(self) ## collect data
        self.decompspor = 0 ## reset sporulation event tally
        self.endospor = 0 ## reset sporulation event tally

    ## add a condition to end model, if no fungi present?




