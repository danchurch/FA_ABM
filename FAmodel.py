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
        for i in range(self.nfungi): 
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            pos = (x, y)
            if any([ type(i)==Fungus for i in self.grid.get_cell_list_contents(pos) ]):
                pass  ## change this to add to cellulose of existing wood
            elif any([ type(i)==Wood for i in self.grid.get_cell_list_contents(pos) ]):
                fungus = Fungus(i, self, pos)
                self.schedule.add(fungus) 
                self.grid.place_agent(fungus, (x,y))


########
#    def make_fungi(self):
#        while sum([ type(i)==Fungus for i in self.schedule.agents ]) < self.nfungi:
#            x = random.randrange(self.grid.width)
#            y = random.randrange(self.grid.height)
#            pos = (x, y)
#            if any([ type(i)==Fungus for i in self.grid.get_cell_list_contents(pos) ]):
#                pass  ## change this to add to cellulose of existing wood
#            else:
#                fungus = Fungus(i, self, pos)
#                self.schedule.add(fungus) 
#                self.grid.place_agent(fungus, (x,y))
#        else: 
#            pass
#
    def step(self): self.schedule.step() 




###############################
## works
#    def make_fungi(self):
#        for i in range(self.nfungi): 
#            x = random.randrange(self.grid.width)
#            y = random.randrange(self.grid.height)
#            pos = (x, y)
#            fungus = Fungus(i, self, pos)
#            self.schedule.add(fungus) 
#            self.grid.place_agent(fungus, (x,y))
#############################

if __name__ == '__main__': 
    losced = Forest(5)
    losced.step()


## so when placing plants, make sure there are no other plants
## when placing wood, if there is already wood, just add to cellulose
## when placing fungi, make sure there is a tree or wood...
## if there is already fungi there? not sure, deal with this
## tomorrow. 


## add some agents manually
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

sum([ type(i)==Fungus for i in losced.schedule.agents ]) < losced.nfungi

sum([ type(i)==Fungus for i in self.schedule.agents ])

dir()

losced.schedule.agents

sum([ type(i)==Wood for i in losced.schedule.agents ])

sum([ type(i)==Wood for i in losced.schedule.agents ]) < 7

aa = []
while sum(aa) < 20:
    print(aa)
    aa.append(1)
else:
    print("done")






