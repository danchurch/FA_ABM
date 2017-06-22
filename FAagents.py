## agents for the FA model:

import random
from numpy import array
from math import exp
from mesa import Agent


##### trees ######
class Tree (Agent):
    def __init__(self, unique_id, model, 
            pos, 
            infection,
            leaffall, 
            disp, 
            endoloss, 
            ):
        super().__init__(unique_id, model)
        self.pos = pos
        self.D = disp ## how far do leaves fall?
        self.infection = infection ## has an endophyte infection?
        self.leaffall = leaffall ## how often do leaves drop? 1=every step, 2=every other, etc.
        self.endoloss = endoloss ## stochastic loss of endophyte infection

    def distancefrom(self, other):
        from numpy import array
        a = array(self.pos)
        b = array(other.pos)
        c = a-b
        d = (c[0]**2+c[1]**2)**(1/2)
        return(d)

    def dropleaves(self):
        if self.infection == True:
            woods = self.model.getall(Wood)
            for ag in woods:
                self.leaf_infect(ag)

    def leaf_infect(self, host):
        if self.model.endophytism:
                dist = self.distancefrom(host)
                prob = exp(-(1/(self.D+0.00001))*dist) ## add a little to keep from dividing by zero
                fname = len(self.model.getall(Fungus)) + 1
                ## tree (leaf) infection of wood
                if type(host)==Wood:
                    if random.random() < prob:
                        fungus = Fungus(fname, self.model, host.pos, endocomp=True, disp=self.model.endodisp)
                        self.model.schedule.add(fungus)
                        self.model.grid.place_agent(fungus, host.pos)
                        fname += 1
                    else: pass
        else: pass 

    def die(self):
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)

    def step(self):
        if self.model.schedule.time % self.leaffall ==  0: ## leaf drop
            self.dropleaves()
        if self.infection == True and random.random() < self.endoloss: ## endohpyte infection loss
            self.infection = False
 

##### fungi ########

class Fungus (Agent):
    def __init__(self, 
                unique_id, 
                model, 
                pos, 
                endocomp,
                disp,
                energy = 1, 
                ):
        super().__init__(unique_id, model)
        self.pos = pos 
        self.endocomp = endocomp
        self.D = disp
        self.energy = energy 

    def distancefrom(self, other):
        from numpy import array
        a = array(self.pos)
        b = array(other.pos)
        c = a-b
        d = (c[0]**2+c[1]**2)**(1/2)
        return(d)

    def die(self):
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)

    def eat(self):
        ## find the wood:
        aa = array(self.model.grid.get_cell_list_contents(self.pos))
        bb = array([ type(i)==Wood for i in aa ], dtype=bool)
        if any(bb): ## if there are any wood on the cell...
            mywood = aa[bb][0] 
            mywood.energy -= 1 ## wood loses energy
            self.energy += 1 ## fungi gets energy
        elif self.energy > 1: ## if no wood present the respiration clock starts because...
            self.energy -= 1 ## energy reserves begin to erode
        elif self.energy < 1: ## and die if energy is less than one
            self.die() 



## wait. they die if no wood? Shouldn't they just die if no energy? fix


    def sporulate(self):
        woods = self.model.getall(Wood)
        for i,ag in enumerate(woods):
            self.spore_infect(ag)
        if self.model.endophytism and self.endocomp:
            trees = self.model.getall(Tree)
            for i,ag in enumerate(trees):
                self.spore_infect(ag)
        else: pass

    def spore_infect(self, host):
        dist = self.distancefrom(host)
        prob = exp(-(1/(self.D+0.00001))*dist)
        fname = len(self.model.getall(Fungus)) + 1
        ## fungus infecting wood
        if type(host)==Wood and dist>0: ## don't allow reinfection feedback, dist > 0
            if random.random() < prob*(host.energy/host.startenergy): ## reduce likelihood if already infected
                fungus = Fungus(fname, self.model, host.pos, endocomp=self.endocomp, disp = self.model.decompdisp)
                self.model.schedule.add(fungus)
                self.model.grid.place_agent(fungus, host.pos)
                fname += 1
            else: pass
        ## fungus infecting tree
        elif type(host)==Tree:
            if random.random() < prob:
                host.infection = True
                fname += 1
            else: pass
        else:
            pass

    def step(self):
        if self.energy > 4:
            self.sporulate()
            print (self.energy)
            if self.endocomp: self.model.endospor += 1
            else: self.model.decompspor += 1 
            self.energy -= 4
            print (self.energy)
        self.eat()


###### wood #########

class Wood (Agent):
    def __init__(self, unique_id, model, pos, energy): 
        super().__init__(unique_id, model)
        self.energy = energy
        self.startenergy = energy
        self.pos = pos
    def die(self):
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)
    def step(self):
        if self.energy < 1: self.die()


