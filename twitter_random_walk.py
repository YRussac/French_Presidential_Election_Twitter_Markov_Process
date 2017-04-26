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

folders = ["seize_avril", "vingt_trois_avril_19_20", "vingt_trois_avril_21_24"]

folder = folders[2]

os.chdir(os.path.join(os.getcwd(), folder))

Metropolis, PageRank = True, True

if 'undirected_graph_{}.json'.format(folder) not in os.listdir(os.getcwd()):

    with open('{}.txt'.format(folder), 'r') as lines:
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

    with open('directed_graph_{}.json'.format(folder), 'w') as g:
        json.dump(directed_graph, g)
    g.close()

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

    with open('id_to_name_{}.json'.format(folder), 'w') as f:
        json.dump(id_to_name, f)
    f.close()

    with open('undirected_graph_{}.json'.format(folder), 'w') as fp:
        json.dump(undirected_graph, fp)
    fp.close()


# Metropolis
if Metropolis:
    with open('undirected_graph_{}.json'.format(folder), 'r') as fp:
        undirected_graph = json.load(fp)
    fp.close()

    epsilon, pathological_nodes, number_of_return_times = graph_centrality(undirected_graph, 1, verbose=False)

    with open('epsilon_M_{}.json'.format(folder), 'w') as fp:
        json.dump(epsilon, fp)
    fp.close()

    with open('pathological_nodes_M_{}.json'.format(folder), 'w') as fq:
        json.dump(pathological_nodes, fq)
    fq.close()

    with open('number_of_return_times_M_{}.json'.format(folder), 'w') as fr:
        json.dump(number_of_return_times, fr)
    fr.close()

# PageRank
if PageRank:

    with open('directed_graph_{}.json'.format(folder), 'r') as fp:
        directed_graph = json.load(fp)
    fp.close()

    epsilon, pathological_nodes, number_of_return_times = graph_centrality(directed_graph, 5000, verbose=False, method="P")

    with open('epsilon_P_{}.json'.format(folder), 'w') as fp:
        json.dump(epsilon, fp)
    fp.close()

    with open('pathological_nodes_P_{}.json'.format(folder), 'w') as fq:
        json.dump(pathological_nodes, fq)
    fq.close()

    with open('number_of_return_times_P_{}.json'.format(folder), 'w') as fr:
        json.dump(number_of_return_times, fr)
    fr.close()
