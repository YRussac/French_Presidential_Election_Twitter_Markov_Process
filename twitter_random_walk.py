# -*- coding: utf-8 -*-

# Main file

import json
import datetime
import matplotlib.pyplot as plt
from graph_functions import links, directed_to_undirected, connected, connected_components
from centrality_functions import graph_centrality


# Parsing
l = []
with open('test.txt', 'r') as f:
    for line in f:
        if "ℵ" not in line:
            l.append(line)
    #l = f.read().split('\nℵ\n')
f.close()

dict_list = [json.loads(j) for j in l]

# List of dictionaries (one dictionary for each node/user)
nodes_list = dict_list[:-1]

# Dictionary in which the keys are the user_id and the values the number of times the user appeared while scraping
users_count = dict_list[-1]

# Associates to each user the users he mentioned or was mentioned by.
directed_graph = {nodes_list[i]['id']: links(nodes_list, i, users_count) for i in range(0, len(nodes_list))}

# Transforms the directed graph into an undirected graph
undirected_graph = directed_to_undirected(directed_graph)

# Plot histogram (niehgbors per node)
# h = [len(undirected_graph[key]) for key in undirected_graph.keys() if len(undirected_graph[key]) < 10]
# plt.hist(h, bins=50)
# plt.show()


# components = connected_components(undirected_graph)
# print([comp[1] for comp in components], sum([comp[1] for comp in components]), len(undirected_graph))


epsilon, mu, sigma = graph_centrality(undirected_graph, 10, nodes_list, verbose=True)

l = []

for key in sigma.keys():
    if len(sigma[key]) > 10:
        l.append((key, sigma[key][-1]))

l.sort(key=lambda tup: tup[1])

print(l)
