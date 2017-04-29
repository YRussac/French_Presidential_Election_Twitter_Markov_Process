# Compute centralities

import json
import numpy as np
import matplotlib.pyplot as plt
from graph_functions import users_hashtag
import pandas as pd
import os

folders = ["seize_avril", "vingt_trois_avril_19_20", "vingt_trois_avril_21_24"]

folder = folders[2]

os.chdir(os.path.join(os.getcwd(), folder))

with open('epsilon_M_{}.json'.format(folder), 'r') as f:
    epsilon_M = json.load(f)
f.close()

with open('epsilon_P_{}.json'.format(folder), 'r') as f:
    epsilon_P = json.load(f)
f.close()

with open('pathological_nodes_M_{}.json'.format(folder), 'r') as f:
    pathological_nodes_M = json.load(f)
f.close()

with open('pathological_nodes_P_{}.json'.format(folder), 'r') as f:
    pathological_nodes_P = json.load(f)
f.close()


# epsilon, pathological_nodes = epsilon[0], epsilon[1]

with open('id_to_name_{}.json'.format(folder), 'r') as f:
    id_to_name = json.load(f)
f.close()

with open('undirected_graph_{}.json'.format(folder), 'r') as f:
    undirected_graph = json.load(f)
f.close()

mu = {node: np.mean(epsilon_M[node][50:]) for node in epsilon_M if node not in pathological_nodes_M}
sigma = {node: np.std(epsilon_M[node][50:], ddof=1) for node in epsilon_M if node not in pathological_nodes_M}
stationary_proba = {node: 1./np.mean(epsilon_P[node][50:]) for node in epsilon_P if node not in pathological_nodes_P}

df_dict = {node: {'mu': mu[node], 'sigma': sigma[node], 'id': id_to_name[node], 'Pagerank': stationary_proba[node]} for node in epsilon_M
           if node not in pathological_nodes_M}

df = pd.DataFrame.from_dict(df_dict, orient='index')
df.to_excel('Centralite_{}.xlsx'.format(folder))

second_order_centrality = [(id_to_name[key], sigma[key]) for key in sigma.keys() if len(epsilon_M[key]) > 1000]
second_order_centrality.sort(key=lambda tup: tup[1])
print(second_order_centrality)


first_order_centrality = [(id_to_name[key], mu[key]) for key in sigma.keys() if len(epsilon_M[key]) > 1000]
first_order_centrality.sort(key=lambda tup: tup[1])
print(first_order_centrality)


if False:
    for key in epsilon_M.keys():
        if len(epsilon_M[key]) > 500:
            s = [np.std(epsilon_M[key][i], ddof=1) for i in range(100, len(epsilon_M[key]))]
            plt.plot(s)
            plt.show()
