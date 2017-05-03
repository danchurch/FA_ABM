from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from FAagents import Tree, Wood, Fungus
from FAmodel import Forest

def agent_portrayal(agent):
    if agent is None: 
        return
    if type(agent) is Tree:
        portrayal = {
            "Shape":"circle", 
            "Color": "#00AA00",
            "Layer": 0,
            "Filled": "true",
            "r" : 1, 
            }
        return portrayal
    elif type(agent) is Fungus: 
        portrayal = {
                "Shape":"circle", 
                "Color": "Red",
                "Layer": 2,
                "Filled": "true",
                "r": .5,
                }
        return portrayal
    else:
        portrayal = {
            "Shape":"rect", 
            "Color": "#A52A2A",
            "Layer": 1,
            "Filled": "true",
            "w" : 1, 
            "h" : 0.5,
            }
        return portrayal

canvas_element = CanvasGrid(agent_portrayal, 10,10,200,200)

server = ModularServer(Forest, [canvas_element], "TreesFungiWood", ts=3)


