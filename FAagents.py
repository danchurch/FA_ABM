## agents for the FA model:

import random
from numpy import array
from math import exp
from mesa import Agent

##### trees ######
class Tree (Agent):
    def __init__(self, unique_id, model, 
            pos, 
            infection = False,
            leaffall = 4, 
            disp = 0.2, 
            ):
        super().__init__(unique_id, model)
        self.pos = pos
        self.D = disp ## how far do leaves fall?
        self.infection = infection ## has endophyte?
        self.leaffall = leaffall ## how often do leaves drop? 1=every step, 2=every other, etc.

    def distancefrom (self, otherpos):
        from math import hypot
        a = array(self.pos)
        b = array(otherpos)
        c = a-b
        return(hypot(c[0],c[1]))

    def getwoods(self): 
        iswood = array([ type(i)==Wood for i in self.model.schedule.agents ])
        ags = array(self.model.schedule.agents)
        return list(ags[iswood])

    def dropleaves(self):
        if self.infection == True:
            woods = self.getwoods()
            for ag in woods:
                self.infect(ag)
        
    def infect(self, host):
        dist = self.distancefrom(host.pos)
        prob = exp(-self.D*dist)
        if type(host)==Wood:
            if random.random() < prob:
                fname = sum([ type(i)==Fungus for i in self.model.schedule.agents ]) + 1
                fungus = Fungus(fname, self.model, host.pos, endocomp=True)
                print("New fungus born:", fungus.unique_id)
                self.model.schedule.add(fungus)
                self.model.grid.place_agent(fungus, host.pos)
                print("Log colonized from a leaf!")
        elif type(host)==Tree:
            if random.random() < prob:
                host.infection = True
                print("Tree infected!")
        else: pass


    def step(self):
        if self.model.schedule.time % self.leaffall ==  0: 
            self.dropleaves()
            print("drop leaves!")
#        print(self.unique_id, self.pos, type(self)) 

##### fungi ########
class Fungus (Agent):
    def __init__(self, 
                unique_id, 
                model, pos, 
                energy = 10, 
                disp = 0.5, 
                endocomp = False):
        super().__init__(unique_id, model)
        self.energy = energy 
        self.endocomp = endocomp 
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

    ## list of wood on the landscape
    def getwoods(self): 
        iswood = array([ type(i)==Wood for i in self.model.schedule.agents ])
        ags = array(self.model.schedule.agents)
        return list(ags[iswood])

    def gettrees(self):
        istree = array([ type(i)==Tree for i in self.model.schedule.agents ])
        ags = array(self.model.schedule.agents)
        return list(ags[istree])

    def distancefrom (self, otherpos):
        from math import hypot
        a = array(self.pos)
        b = array(otherpos)
        c = a-b
        return(hypot(c[0],c[1]))

    def infect(self, host):
        dist = self.distancefrom(host.pos)
        prob = exp(-self.D*dist) 
        if type(host)==Wood:
            ## for wood, reduce the probability by the amount of energy 
            ## already consumed (~ competition, smaller target)
            if random.random() < prob*(host.energy/host.startenergy):
                fname = sum([ type(i)==Fungus for i in self.model.schedule.agents ]) + 1
                fungus = Fungus(fname, self.model, host.pos, endocomp=self.endocomp)
                print("New fungus born:", fungus.unique_id)
                self.model.schedule.add(fungus)
                self.model.grid.place_agent(fungus, host.pos)
                print("Log inocculated!")
        elif type(host)==Tree:
            if random.random() < prob:
                host.infection = True
                print("Tree infected!")
        else: pass

    def sporulate(self):
        print("sporulation happening!")
        woods = self.getwoods()
        for i,ag in enumerate(woods):
            self.infect(ag)
        if self.endocomp==True:
            trees = self.gettrees()
            for i,ag in enumerate(trees):
                self.infect(ag)

    def step(self):
        if self.energy > 3:
            self.sporulate()
            self.energy -= 3
        self.eat()
#        print(self.unique_id, self.pos, type(self), "E:", self.energy) 


###### wood #########
class Wood (Agent):
    def __init__(self, unique_id, model, pos, energy = 10): 
        super().__init__(unique_id, model)
        self.energy = energy
        self.startenergy = energy
        self.pos = pos
    def die(self):
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)
    def step(self):
#        print(self.unique_id, self.pos, type(self), "E:", self.energy) 
        if self.energy < 1: self.die()

###### to do ######

## wood deposition - random or function of trees?
## reduction in likelihood of infection if already 
    ## colonized by other fungi 
## fix graphics - fungi on top of each other

