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




