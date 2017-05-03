## txtbook for first attempts at a FA ABM:

## can we put them in a landscape?

from mesa import Agent, Model
from mesa.time import RandomActivation
import random
import numpy as np
import matplotlib.pyplot as plt
from mesa.space import MultiGrid
from mesa.time import RandomActivation

###### model #######
class Forest (Model): 
    def __init__ (self, ts=10, fs=2, ws = 5, width = 10, height = 10):
        self.ntrees = ts 
        self.nfungi = fs 
        self.nwood = ws 
        self.schedule = RandomActivation(self) 
        self.grid = MultiGrid(width, height, torus = True)
        for i in range(self.nfungi): 
            x = random.randrange(width)
            y = random.randrange(height)
            pos = (x, y)
            fungus = Fungus(i, self, pos)
            self.schedule.add(fungus) 
            self.grid.place_agent(fungus, (x,y))
        for i in range(self.ntrees): 
            x = random.randrange(width)
            y = random.randrange(height)
            pos = (x, y)
            tree = Tree(i, self, pos)
            self.schedule.add(tree) 
            self.grid.place_agent(tree, (x,y))
        for i in range(self.ntrees): 
            x = random.randrange(width)
            y = random.randrange(height)
            pos = (x, y)
            wood = Wood(i, self, pos)
            self.schedule.add(wood) 
            self.grid.place_agent(wood, (x,y))
    def step(self): self.schedule.step() 

##### trees ######
class Tree (Agent):
    def __init__(self, unique_id, model, pos, leaffall = 1, leafdist = 1, woodfall = 1, wooddist = 1):
        super().__init__(unique_id, model)
        self.leaffall = leaffall
        self.leafdist = leafdist
        self.woodfall = woodfall
        self.wooddist = wooddist
        self.pos = pos
    def dropleaves(self): pass 
    def dropbranch(self): pass 
    def die(self): pass 
    def step(self):
        print(self.unique_id, self.pos, type(self)) 

##### fungi ########
class Fungus (Agent):
    def __init__(self, unique_id, model, pos, energy = 3, endocomp = "yes", lifestage = "D", sporedist=3):
        super().__init__(unique_id, model)
        self.energy = energy 
        self.endocomp = endocomp 
        self.lifestage = lifestage 
        self.sporedist = sporedist
        self.pos = pos 
    def sporulate(self): pass
    def step(self):
        print(self.unique_id, self.pos, type(self)) 
        #pass 

###### wood #########
class Wood (Agent):
    def __init__(self, unique_id, model, pos, cellulose = 10): 
        super().__init__(unique_id, model)
        self.cellulose = cellulose
    def step(self):
        print(self.unique_id, self.pos, self.cellulose, type(self)) 

## test
if __name__ == '__main__':
    losced = Forest(3)
    losced.step()


