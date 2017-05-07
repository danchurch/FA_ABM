from mesa import Agent, Model
from mesa.time import RandomActivation
import random
import numpy as np
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from FAagents import Tree, Wood, Fungus

###### model #######
class Forest (Model): 
    def __init__ (self, ts=10, ndecomp=1, nendo=1, ws = 5, width = 10, height = 10):
        self.ntrees = ts 
        self.ndecomp = ndecomp 
        self.nendo = nendo 
        self.nwood = ws 
        self.schedule = RandomActivation(self) 
        self.grid = MultiGrid(width, height, torus = True)
        self.running = True
        self.make_trees()
        self.make_wood()
        self.make_fungi()


    def make_trees(self):
        wname = 1
        while sum([ type(i)==Tree for i in self.schedule.agents ]) < self.ntrees:
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            pos = (x, y)
            ## check for tree already present:
            if any([ type(i)==Tree for i in self.grid.get_cell_list_contents(pos) ]):
                pass  ## but this will result in one fewer tree than normal!
            else: 
                tree = Tree(wname, self, pos)
                self.schedule.add(tree) 
                self.grid.place_agent(tree, (x,y))
                wname += 1



    def make_wood(self):
        for i in range(self.nwood): 
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            pos = (x, y)
            if any([ type(i)==Wood for i in self.grid.get_cell_list_contents(pos) ]):
                pass  ## change this to add to energy of existing wood
            else:
                wood = Wood(i, self, pos)
                self.grid.place_agent(wood, (x,y))
                self.schedule.add(wood) 


    def make_fungi(self):
        fname = sum([ type(i)==Fungus for i in self.schedule.agents ]) + 1

        ## decomposers first:
        while sum([ type(i)==Fungus for i in self.schedule.agents ]) < self.ndecomp:
            pos = self.findsubstrate(Wood)
            if any([ type(i)==Fungus for i in self.grid.get_cell_list_contents(pos) ]):
                pass  ## change this to add to energy of existing wood
            else:
                fungus = Fungus(fname, self, pos, endocomp=False)
                self.schedule.add(fungus) 
                self.grid.place_agent(fungus, pos)
                fname += 1

        ## then endophytes:
        while sum([ type(i)==Fungus for i in self.schedule.agents ]) < self.ndecomp + self.nendo:
            pos = self.findsubstrate(Wood)
            if any([ type(i)==Fungus for i in self.grid.get_cell_list_contents(pos) ]):
                pass  ## change this to add to energy of existing wood
            else:
                fungus = Fungus(fname, self, pos, endocomp=True)
                self.schedule.add(fungus) 
                self.grid.place_agent(fungus, pos)
                fname += 1


    ## for finding wood to place fungi on, maybe useful for sporulation?
    def findsubstrate (self, substrate):
        sub = [ type(i)==substrate for i in self.schedule.agents ]  ## is wood?
        subnp = np.array(sub, dtype=bool) ## np array, boolean
        Agnp = np.array(self.schedule.agents) ## np array of agents
        Subs = Agnp[subnp] ## filter using our iswood? boolean array
        return(random.choice(Subs).pos) ## pick from these, return position

    def step(self): self.schedule.step() 

###works##############
#
#    def make_fungi(self):
#        fname = len(self.schedule.agents) + 1
#        while sum([ type(i)==Fungus for i in self.schedule.agents ]) < self.nfungi:
#            pos = self.findsubstrate(Wood)
#            if any([ type(i)==Fungus for i in self.grid.get_cell_list_contents(pos) ]):
#                pass  ## change this to add to energy of existing wood
#            else:
#                fungus = Fungus(fname, self, pos)
#                self.schedule.add(fungus) 
#                self.grid.place_agent(fungus, pos)
#                fname += 1
#
