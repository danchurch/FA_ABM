from mesa import Agent, Model
from mesa.time import RandomActivation
import random
import numpy as np
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from FAagents import Tree, Wood, Fungus

###### model #######
class Forest (Model): 
    def __init__ (self, ts=10, ndecomp=1, 
                nendo=1, ws = 5, 
                woodfreq = 4, 
                newwood = 4, width = 10, 
                height = 10):
        self.ntrees = ts 
        self.ndecomp = ndecomp 
        self.nendo = nendo 
        self.nwood = ws 
        self.newwood = newwood 
        self.woodfreq = woodfreq
        self.schedule = RandomActivation(self) 
        self.grid = MultiGrid(width, height, torus = True)
        self.running = True
        self.make_trees()
        for i in range(self.nwood): self.add_wood()
        self.make_fungi()


    def make_trees(self):
        tname = 1
        while sum([ type(i)==Tree for i in self.schedule.agents ]) < self.ntrees:
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            pos = (x, y)
            ## check for tree already present:
            if any([ type(i)==Tree for i in self.grid.get_cell_list_contents(pos) ]):
                pass  
            else: 
                tree = Tree(tname, self, pos)
                self.schedule.add(tree) 
                self.grid.place_agent(tree, (x,y))
                tname += 1



    def add_wood(self):
        wname = sum([ type(i)==Wood for i in self.schedule.agents ]) + 1
        x = random.randrange(self.grid.width)
        y = random.randrange(self.grid.height)
        pos = (x, y)
        ## wood already present? then just add to the pile
        if any([ type(i)==Wood for i in self.grid.get_cell_list_contents(pos) ]):
            for i in self.grid.get_cell_list_contents(pos):
                if type(i)==Wood: 
                    i.energy += 3
                    print("Adding to the pile!")
        else:
            wood = Wood(wname, self, pos)
            self.grid.place_agent(wood, (x,y))
            self.schedule.add(wood)
            print("new log!")
            wname += 1 

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

    def step(self): 
        if self.schedule.time % self.woodfreq ==  3:
            for i in range(random.randrange(self.newwood)): self.add_wood()
        self.schedule.step() 



