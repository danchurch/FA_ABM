from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from FAAB import Forest, Tree

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle", 
        "r":.75,
        "Color": "Red",
        "Layer": 0,
        "Filled": "true",
        }
    return portrayal

canvas_element = CanvasGrid(agent_portrayal, 10,10,200,200)

server = ModularServer(Forest, [canvas_element], "Trees", ts=3)


