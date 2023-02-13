#This file creates the plot for the nodes
import networkx as nx
import matplotlib.pyplot as plt
import json
from matplotlib.figure import Figure
from tkinter.messagebox import showinfo

G = nx.Graph()
def plot():
    print("Plotting graph")
    path = "assets/startup/config.json"
    # Build a dataframe with your connections
    with open(path, 'r') as openfile:
        json_object = json.load(openfile)
        link = json_object["links"]

    G.clear()
    plt.clf()
    # Build your graph
    G.add_nodes_from(link['nodes'])
    G.add_edges_from(link['edges'])
    
    # Graph with Custom nodes:
    nx.draw(G, with_labels=True, node_size=200, node_color="skyblue", node_shape="s", alpha=0.8, linewidths=40, edge_color="red")
    
    # plt.show()
    plt.savefig("assets/nodes.png", 
                bbox_inches='tight'
                # dpi = 200
                )
    
    return "assets/nodes.png"

def add_edge(edgefrom,edgeto):
    path = "assets/startup/config.json"
    
    if edgefrom == edgeto:
        print("Cannot add edge to same object")
        return
    
    with open(path, 'r') as openfile:
        json_object = json.load(openfile)
        link = json_object["links"]
    
    temp = [edgefrom,edgeto]
    
    if [edgefrom,edgeto] in link['edges'] or [edgeto,edgefrom] in link['edges']:
        print ("Edge already added")
        showinfo(
            title='Error Adding',
            message="A link already exists between\nthe selected devices"
        )
        return
    
    link["edges"].append(temp)

    json_object["links"] = link
    
    with open(path, "w") as outfile:
        json.dump(json_object, outfile, indent= 4)
        print ("Edge added successfully")
    plot()

def neighbors(name):
    return list(G.neighbors(name))