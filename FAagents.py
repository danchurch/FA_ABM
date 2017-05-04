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
    def eat(self):
        self.energy += 1 ## fungi gets energy
        ## find the wood:
        aa = np.array(self.model.grid.get_cell_list_contents(pos))
        bb = np.array([ type(i)==Wood for i in aa ], dtype=bool)
        mywood = aa[bb][0]
        mywood.cellulose -= 1 ## wood loses cellulose
    def step(self):
        self.eat()
        print(self.unique_id, self.pos, type(self), "E:", self.energy) 
        #pass 

###### wood #########
class Wood (Agent):
    def __init__(self, unique_id, model, pos, cellulose = 10): 
        super().__init__(unique_id, model)
        self.cellulose = cellulose
        self.pos = pos
    def step(self):
        print(self.unique_id, self.pos, type(self), "C:", self.cellulose) 




if __name__ == '__main__':
    from FAmodel import Forest
    import random
    losced = Forest(5)
    losced.step()

## fungus eating - whereever a fungi is on a log, fungus 
## gets one unit of energy, log loses one unit of cellulose

def eat(self):
    self.energy += 1


## how to find the cellulose of a given fungi's substrate?
## we know there is wood there. How to access it by location?








