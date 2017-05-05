## agents for the FA model:

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
    def __init__(self, unique_id, model, pos, energy = 3, endocomp = "yes", lifestage = "D", sporedist=3):
        super().__init__(unique_id, model)
        self.energy = energy 
        self.endocomp = endocomp 
        self.lifestage = lifestage 
        self.sporedist = sporedist
        self.pos = pos 
    def sporulate(self): pass
    def die(self):
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)
    def eat(self):
        from numpy import array
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
    def step(self):
        self.eat()
        print(self.unique_id, self.pos, type(self), "E:", self.energy) 
        #pass 

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
