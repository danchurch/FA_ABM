from mesa import Agent, Model
from mesa.time import RandomActivation
import random
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
            tree = Tree(i, self, pos)
            self.schedule.add(tree) 
            self.grid.place_agent(tree, (x,y))
    def step(self): self.schedule.step() 
    def make_wood(self):
        for i in range(self.nwood): 
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            pos = (x, y)
            wood = Wood(i, self, pos)
            self.schedule.add(wood) 
            self.grid.place_agent(wood, (x,y))
    def make_fungi(self):
        for i in range(self.nfungi): 
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            pos = (x, y)
            fungus = Fungus(i, self, pos)
            self.schedule.add(fungus) 
            self.grid.place_agent(fungus, (x,y))

if __name__ == '__main__': 
    losced = Forest(5)
    losced.step()
