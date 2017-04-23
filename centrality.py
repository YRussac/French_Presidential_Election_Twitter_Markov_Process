# Compute centralities

import json
import numpy as np
import matplotlib.pyplot as plt
from graph_functions import users_hashtag
import pandas as pd

with open('epsilon.json', 'r') as f:
    epsilon = json.load(f)
f.close()

with open('pathological_nodes.json', 'r') as f:
    pathological_nodes = json.load(f)
f.close()

# epsilon, pathological_nodes = epsilon[0], epsilon[1]

with open('id_to_name.json', 'r') as f:
    id_to_name = json.load(f)
f.close()

with open('undirected_graph.json', 'r') as f:
    undirected_graph = json.load(f)
f.close()

nodes = epsilon.keys()

mu = {node: np.mean(epsilon[node][500:]) for node in epsilon if node not in pathological_nodes}
sigma = {node: np.std(epsilon[node][500:], ddof=1) for node in epsilon if node not in pathological_nodes}

df_dict = {node: {'mu': mu[node], 'sigma': sigma[node], 'id': id_to_name[node]} for node in epsilon
           if node not in pathological_nodes}

df = pd.DataFrame.from_dict(df_dict, orient='index')
df.to_excel('Centralite.xlsx')

second_order_centrality = [(id_to_name[key], sigma[key]) for key in sigma.keys() if len(epsilon[key]) > 1000]
second_order_centrality.sort(key=lambda tup: tup[1])
print(second_order_centrality)


first_order_centrality = [(id_to_name[key], mu[key]) for key in sigma.keys() if len(epsilon[key]) > 1000]
first_order_centrality.sort(key=lambda tup: tup[1])
print(first_order_centrality)



for key in epsilon.keys():
    if len(epsilon[key]) > 500:
        s = [np.std(epsilon[key][i], ddof=1) for i in range(100, len(epsilon[key]))]
        plt.plot(s)
        plt.show()
