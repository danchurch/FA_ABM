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
                endophytism = True, ## allow endophyte life style in model run
                ws = 30, 
                endodisp=1,
                decompdisp=10, 
                leafdisp = 4, 
                leaffall = 1, 
                numdecomp=1, 
                numendo=1,   
                endoloss=0.05,   
                newwood = 6, 
                woodfreq = 1, 
                width = 100, 
                kappa = 0.03, 
                sigma = 3.0, 
                mu = 2.2, 
                        )
