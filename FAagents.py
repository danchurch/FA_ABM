## agents for the FA model:

import random
from numpy import array
from math import exp
from mesa import Agent

##### trees ######
class Tree (Agent):
    def __init__(self, unique_id, model, 
            pos, 
            leaffall = 1, 
            leafdist = 1, 
            woodfall = 1, 
            wooddist = 1,
            ):
        super().__init__(unique_id, model)
        self.leaffall = leaffall
        self.leafdist = leafdist
        self.woodfall = woodfall
        self.wooddist = wooddist
        self.pos = pos
    def dropleaves(self): pass 
    def dropbranch(self): pass 
    def step(self):
        print(self.unique_id, self.pos, type(self)) 

##### fungi ########
class Fungus (Agent):
    def __init__(self, 
                unique_id, 
                model, pos, 
                energy = 3, 
                disp = 0.5, 
                endocomp = "yes", 
                lifestage = "D", 
                sporedist=3):
        super().__init__(unique_id, model)
        self.energy = energy 
        self.endocomp = endocomp 
        self.lifestage = lifestage 
        self.D = disp
        self.pos = pos 

    def die(self):
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)

    def eat(self):
        self.energy += 1 ## fungi gets energy
        ## find the wood:
        aa = array(self.model.grid.get_cell_list_contents(self.pos))
        bb = array([ type(i)==Wood for i in aa ], dtype=bool)
        if any(bb):
            mywood = aa[bb][0]
            mywood.energy -= 1 ## wood loses energy
        else: 
            print("Dead!")
            self.die()

    def getwoods(self):
        iswood = array([ type(i)==Wood for i in self.model.schedule.agents ])
        ags = array(self.model.schedule.agents)
        return list(ags[iswood])

    def distancefrom (self, otherpos):
        from math import hypot
        a = array(self.pos)
        b = array(otherpos)
        c = a-b
        return(hypot(c[0],c[1]))

    def infectwood(self, wood):
        dist = self.distancefrom(wood.pos)
        prob = exp(-self.D*dist)
        if random.random() < prob:
            fname = len(self.model.schedule.agents)+1
            fungus = Fungus(fname, self, wood.pos)
            self.model.schedule.add(fungus)
            self.model.grid.place_agent(fungus, wood.pos)
            print("Another log inocculated!")
        else: pass

    def sporulate(self):
        woods = self.getwoods()
        for i,ag in enumerate(woods):
            self.infectwood(ag)


    def findsubstrate (self, substrate):
        sub = [ type(i)==substrate for i in self.schedule.agents ]  ## is wood?
        subnp = array(sub, dtype=bool) ## array, boolean
        Agnp = array(self.schedule.agents) ## array of agents
        Subs = Agnp[subnp] ## filter using our iswood? boolean array
        return(random.choice(Subs).pos) ## pick from these, return position

    def step(self):
        if self.energy > 3:
            self.sporulate()
            self.energy -= 3
        self.eat()
        print(self.unique_id, self.pos, type(self), "E:", self.energy) 



###### wood #########
class Wood (Agent):
    def __init__(self, unique_id, model, pos, energy = 10): 
        super().__init__(unique_id, model)
        self.energy = energy
        self.pos = pos
    def die(self):
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)
    def step(self):
        print(self.unique_id, self.pos, type(self), "E:", self.energy) 
        if self.energy < 1: self.die()

## need to remove fungi on log
## not sure if removing an agent from the sched and grid 
## removes it from memory space of model
