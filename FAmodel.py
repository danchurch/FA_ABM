from mesa import Agent, Model
from mesa.time import RandomActivation
import random
import numpy as np
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from FAagents import Tree, Wood, Fungus

###### model #######
class Forest (Model): 
    def __init__ (self, ts=10, fs=2, ws = 5, width = 10, height = 10):
        self.ntrees = ts 
        self.nfungi = fs 
        self.nwood = ws 
        self.schedule = RandomActivation(self) 
        self.grid = MultiGrid(width, height, torus = True)
        self.make_trees()
        self.make_wood()
        self.make_fungi()
    def make_trees(self):
        for i in range(self.ntrees): 
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            pos = (x, y)
            ## check for tree already present:
            if any([ type(i)==Tree for i in self.grid.get_cell_list_contents(pos) ]):
                pass  ## but this will result in one fewer tree than normal!
            else: 
                tree = Tree(i, self, pos)
                self.schedule.add(tree) 
                self.grid.place_agent(tree, (x,y))
    def make_wood(self):
        for i in range(self.nwood): 
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            pos = (x, y)
            if any([ type(i)==Wood for i in self.grid.get_cell_list_contents(pos) ]):
                pass  ## change this to add to cellulose of existing wood
            else:
                wood = Wood(i, self, pos)
                self.grid.place_agent(wood, (x,y))
                self.schedule.add(wood) 
############
    def make_fungi(self):
        fname = len(self.schedule.agents) + 1
        while sum([ type(i)==Fungus for i in self.schedule.agents ]) < self.nfungi:
            pos = self.findsubstrate(Wood)
            if any([ type(i)==Fungus for i in self.grid.get_cell_list_contents(pos) ]):
                pass  ## change this to add to cellulose of existing wood
            else:
                fungus = Fungus(fname, self, pos)
                self.schedule.add(fungus) 
                self.grid.place_agent(fungus, pos)
                fname += 1
    def findsubstrate (self, substrate):
        sub = [ type(i)==substrate for i in self.schedule.agents ]  ## is wood?
        subnp = np.array(sub, dtype=bool) ## np array, boolean
        Agnp = np.array(self.schedule.agents) ## np array of agents
        Subs = Agnp[subnp] ## filter using our iswood? boolean array
        return(random.choice(Subs).pos) ## pick from these, return position
###########
    def step(self): self.schedule.step() 


if __name__ == '__main__': 
    losced = Forest(5)
    losced.step()


## add some agents manually
if __name__=='__main__':
    a1 = Fungus(123,Agent, (5,5))
    losced.grid.place_agent(a1, a1.pos)
    losced.schedule.add(a1) 
    a2 = Fungus(124,Agent, (5,5))
    losced.grid.place_agent(a2, a2.pos)
    losced.schedule.add(a2) 
    a3 = Tree(124,Agent, (5,5))
    losced.grid.place_agent(a3, a3.pos)
    losced.schedule.add(a3) 
    pos = (5,5)
    losced.grid.get_cell_list_contents(pos)


