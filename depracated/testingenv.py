# libraries
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
 
# Build a dataframe with your connections
# df = pd.DataFrame({
#                     'nodes':['Router1', 'Router1', 'C','A','E'],
#                     'from':['Router1', 'Router1', 'C','A'], 
#                     'to':['Router1', 'A', 'E','C']
#                    })
data = {
                    'nodes':['Router1', 'Router1', 'C','A','E'],
                    'edges':[('C','A'), 
                            ('E','C')]
                   }
# df = pd.DataFrame(data)

 
# Build your graph
# G=nx.from_pandas_edgelist(df, 'from', 'to')
G = nx.Graph()

G.add_nodes_from(data['nodes'])
G.add_edges_from(data['edges'])
 
# Graph with Custom nodes:
nx.draw(G, with_labels=True, node_size=800, node_color="skyblue", node_shape="s", alpha=0.9, linewidths=40)
plt.show()

# for x in range(3):
#     print (x)
# # How to write to file
# ###################################
# # Data to be written
# router1 = Router()
# file = "assets/running/sample.json"
# # Serializing json
# json_object = json.dumps(router1.__dict__, indent=4)
 
# # Writing to sample.json
# with open(file, "w") as outfile:
#     json.dump(router1.__dict__, outfile, indent= 4)
    
    
# # How to read from it
# ##################################

# with open(file, 'r') as openfile:
 
#     # Reading from json file
#     json_object = json.load(openfile)

# print(json_object["name"])
# print(type(json_object))


# class BottomPanel:
#     def __init__(self, window) -> None:
#         #Adding side pane
#         self.window = window
        
#         self.bottom_panel = PanedWindow(window, bd=4, bg="red", height=100) 
#         self.bottom_panel.pack(fill=X, expand=1, side=BOTTOM)
        
#         self.right_label = Label(self.bottom_panel, text = "Right Panel")
#         self.bottom_panel.add(self.right_label)
        
#         Button(self.bottom_panel, text='Open Terminal', command=self.popup).pack()
    
#     def popup(self):
#         d = simpledialog(self.window)
#         print('opened login window, about to wait')
#         self.window.wait_window(d.root)   # <<< NOTE
#         print('end wait_window, back in MainWindow code')
#         print(f'got data: {d.data}')