from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", 
        "Color": "red", 
        "Filled": "true",
        "Layer": 0,
        "r": 0.5 
        }
    return protrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = ModularServer(Forest, 
                        [grid],
                        "Testing Trees",
                        100, 10, 10
                        )

server.launch()



boid_canvas = SimpleCanvas(boid_draw, 500, 500)
server = ModularServer(BoidModel, [boid_canvas], "Boids",
100, 100, 100, 5, 10, 2)
