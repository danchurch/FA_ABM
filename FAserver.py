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
                "Shape":"tree.png", 
                "Layer": 0,
                "scale": 10,
                }
        if agent.infection == True: 
            portrayal = {
                "Shape":"tree_infected.png", 
                "Layer": 0,
                "scale": 10,
                }
        return portrayal

    elif type(agent) is Fungus: 
        if agent.endocomp == False: 
                portrayal = {
                        "Shape":"redmush_off.png", 
                        "Color": "Blue",
                        "Layer": 2,
                        "scale": 7
                        }
                return portrayal
        else:
                portrayal = {
                        "Shape":"bluemush_off.png", 
                        "Color": "Blue",
                        "Layer": 2,
                        "scale": 7
                        }
                return portrayal
    else:
        portrayal = {
            "Shape":"log.png", 
            "Layer": 1,
            "scale" : 7,
            }
        return portrayal

canvas_element = CanvasGrid(agent_portrayal, 100,100,500,500)

server = ModularServer(Forest, [canvas_element], "TreesFungiWood", ts=30)


