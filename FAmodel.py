from mesa import Agent, Model
from mesa.time import RandomActivation
import random
import numpy as np
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from FAagents import Tree, Wood, Fungus

###### model #######
class Forest (Model): 
    def __init__ (self,  
                ts=30, ws = 20, ## initial num of trees, wood
                endodisp=.01, ## dispersal of endos
                decompdisp=0.01, ## dispersal of decomps
                numdecomp=1, ## initial number of decomposers
                numendo=1,   ## initial number of endos
                newwood = 4, ## amount of logs to put on landscape at a time
                woodfreq = 4, ## how often to put new logs onto the landscape 
                width = 100, height = 100): ## grid dimensions

        self.ntrees = ts 
        self.nwood = ws 
        self.endodisp = endodisp 
        self.decompdisp = decompdisp 
        self.numdecomp = numdecomp 
        self.numendo = numendo 
        self.newwood = newwood 
        self.woodfreq = woodfreq
        self.schedule = RandomActivation(self) 
        self.grid = MultiGrid(width, height, torus = True)
        self.running = True

        ## make initial agents:
        self.make_trees()
        for i in range(self.nwood): self.add_wood() ## no make_woods method
        self.make_fungi()


    def make_trees(self):
        tname = 1
        while len(self.getall(Tree)) < self.ntrees:
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
        wname = len(self.getall(Wood)) + 1 
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
        fname = len(self.getall(Fungus)) + 1 

        ## decomposers first:
        decomps=0
        while decomps < self.numdecomp:
            pos = self.findsubstrate(Wood)
            if any([ type(i)==Fungus for i in self.grid.get_cell_list_contents(pos) ]):
                pass 
            else:
                fungus = Fungus(fname, self, pos, endocomp=False, disp = self.endodisp)
                self.schedule.add(fungus) 
                self.grid.place_agent(fungus, pos)
                fname += 1; decomps += 1

        ## then endophytes:
        #while sum([ i.endocomp==True for i in self.getall(Fungus) ]) < self.numendo:
        endos=0
        while endos < self.numendo:
            pos = self.findsubstrate(Wood)
            if any([ type(i)==Fungus for i in self.grid.get_cell_list_contents(pos) ]):
                pass
            else:
                fungus = Fungus(fname, self, pos, endocomp=True, disp = self.decompdisp)
                self.schedule.add(fungus) 
                self.grid.place_agent(fungus, pos)
                fname += 1; endos += 1


    ## for finding wood to place fungi on, maybe useful for sporulation?
#    def findsubstrate (self, substrate):
#        sub = [ type(i)==substrate for i in self.schedule.agents ]  ## is wood?
#        subnp = np.array(sub, dtype=bool) ## np array, boolean
#        Agnp = np.array(self.schedule.agents) ## np array of agents
#        Subs = Agnp[subnp] ## filter using our iswood? boolean array
#        return(random.choice(Subs).pos) ## pick from these, return position

    def findsubstrate (self, substrate):
        Subs = self.getall(substrate)
        return(random.choice(Subs).pos) ## pick from these, return position

    def getall(self, typeof):
        if not any([ type(i)==typeof for i in self.schedule.agents ]):
            return([])
        else:
            istype = np.array([ type(i)==typeof for i in self.schedule.agents ])
            ags = np.array(self.schedule.agents)
            return list(ags[istype])

    def step(self): 
        if self.schedule.time % self.woodfreq ==  3:
            for i in range(random.randrange(self.newwood)): self.add_wood()
        self.schedule.step() 
    ## add a condition to end model, if no fungi present.



