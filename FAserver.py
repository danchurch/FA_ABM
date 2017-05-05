from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from FAagents import Tree, Wood, Fungus
from FAmodel import Forest

def agent_portrayal(agent):
    if agent is None: 
        return
    if type(agent) is Tree:
        portrayal = {
            "Shape":"tree.png", 
            "Layer": 0,
            "scale": 2,
            }
        return portrayal
    elif type(agent) is Fungus: 
        portrayal = {
                "Shape":"mushroom.png", 
                "Color": "Blue",
                "Layer": 2,
                "scale": 0.75
                }
        return portrayal
    else:
        portrayal = {
            "Shape":"log.png", 
            "Layer": 1,
            "scale" : 1,
            }
        return portrayal

canvas_element = CanvasGrid(agent_portrayal, 10,10,200,200)

server = ModularServer(Forest, [canvas_element], "TreesFungiWood", ts=3)


