from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from FAAB import Forest, Tree, Fungus

def agent_portrayal(agent):
    if agent is None: 
        return
    if type(agent) is Tree:
        portrayal = {
            "Shape":"rect", 
            "Color": "#00AA00",
            "Layer": 0,
            "Filled": "true",
            "w" : 1, 
            "h" : 1,
            }
        return portrayal

    elif type(agent) is Fungus: 
        portrayal = {
                "Shape":"circle", 
                "Color": "Red",
                "Layer": 1,
                "Filled": "true",
                "r": .5,
                }
    return portrayal
     
canvas_element = CanvasGrid(agent_portrayal, 10,10,200,200)

server = ModularServer(Forest, [canvas_element], "Trees", ts=3)

