from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from FAagents import Tree, Wood, Fungus
from FAmodel import Forest

def agent_portrayal(agent):
    if agent is None: 
        return
    if type(agent) is Tree:
        if agent.infection == False: 
            portrayal = {
                "Shape":"graphics/tree.png", 
                "Layer": 0,
                "scale": 5,
                }
        if agent.infection == True: 
            portrayal = {
                "Shape":"graphics/tree_infected.png", 
                "Layer": 0,
                "scale": 5,
                }
        return portrayal

    elif type(agent) is Fungus: 
        if agent.endocomp == False: 
                portrayal = {
                        "Shape":"graphics/redmush_off.png", 
                        "Color": "Blue",
                        "Layer": 2,
                        "scale": 4
                        }
                return portrayal
        else:
                portrayal = {
                        "Shape":"graphics/bluemush_off.png", 
                        "Color": "Blue",
                        "Layer": 2,
                        "scale": 4
                        }
                return portrayal
    else:
        portrayal = {
            "Shape":"graphics/log.png", 
            "Layer": 1,
            "scale" : 4,
            }
        return portrayal

canvas_element = CanvasGrid(agent_portrayal, 100,100,500,500)


server = ModularServer(Forest, [canvas_element], "TreesFungiWood", 
                        decompdisp=5, 
                        endodisp=1, 
                        endoloss=0.25, 
                        newwood = 4,  
                        woodfreq = 1,  
                        )
