# -*- coding: utf-8 -*-

# Main file

import json
import os
import datetime
import matplotlib.pyplot as plt
from graph_functions import links, directed_to_undirected, connected, connected_components
from centrality_functions import graph_centrality

# If we have not created the graph corresponding to the tweets we fetched
# Otherwise we load it
if 'undirected_graph.json' not in os.listdir(os.getcwd()):

    with open('seizeavril.txt', 'r') as lines:
        l = [line for line in lines]
    lines.close()

    dict_list = [json.loads(j) for j in l]

    # List of dictionaries (one dictionary for each node/user)
    nodes_list = dict_list[:-1]

    # Dictionary twitter_id to twitter_name
    id_to_name = {node['id']: node['screen_name'] for node in nodes_list}

    # Dictionary in which the keys are the user_id and the values the number of times the user appeared while scraping
    users_count = dict_list[-1]

    # Associates to each user the users he mentioned or was mentioned by
    directed_graph = {nodes_list[i]['id']: links(nodes_list, i, users_count) for i in range(0, len(nodes_list))}

    # Transforms the directed graph into an undirected graph
    undirected_graph = directed_to_undirected(directed_graph)

    # Plot histogram (neighbors per node)
    # h = [len(undirected_graph[key]) for key in undirected_graph.keys() if len(undirected_graph[key]) < 10]
    # plt.hist(h, bins=50)
    # plt.show())

    # We test if the graph is connected, if not we remove the small unconnected graph
    v, explored_nodes, unexplored_nodes = connected(undirected_graph)

    for node in unexplored_nodes:
        undirected_graph.pop(node)

    # components = connected_components(undirected_graph)
    # print([comp[1] for comp in components], sum([comp[1] for comp in components]), len(undirected_graph))

    with open('id_to_name.json', 'w') as f:
        json.dump(id_to_name, f)
    f.close()

    with open('undirected_graph.json', 'w') as fp:
        json.dump(undirected_graph, fp)
    fp.close()

else:
    with open('undirected_graph.json', 'r') as fp:
        undirected_graph = json.load(fp)
    fp.close()


epsilon, pathological_nodes = graph_centrality(undirected_graph, 3500, verbose=False)

with open('epsilon.json', 'w') as fp:
    json.dump(epsilon, fp)
fp.close()

with open('pathological_nodes.json', 'w') as fq:
    json.dump(pathological_nodes, fq)
fq.close()
