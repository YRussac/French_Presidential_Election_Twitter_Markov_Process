# -*- coding: utf-8 -*-
from random import randint
from random import uniform, seed
import sys
import numpy as np
import json
import datetime
import matplotlib.pyplot as plt

# Parsing
l=[]
with open('saved_info.txt', 'r') as f:
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


#
def links(users_list, n, users_id):
    """
    for user in position n in nodes_list we get all the users of the hashtags he mentionned
    """
    m = []
    # On parcourt les tweets d'un user n donné
    for i in range(0, len(users_list[n]['tweets'])):

        # Pour chaque tweet on parcourt les utilisateurs mentionnes
        for j in range(0, len(users_list[n]['tweets'][i]['user_mentions'])):

            # si un utilisateur mentionné est dans la liste qui contient tous les users qui ont utilisé un des hashtags
            if users_list[n]['tweets'][i]['user_mentions'][j] in users_id:   
                if users_list[n]['tweets'][i]['user_mentions'][j] not in m and users_list[n]['tweets'][i]['user_mentions'][j] != users_list[n]['id']:
                    m.append(users_list[n]['tweets'][i]['user_mentions'][j])
    return m

# Associates to each user the users he mentioned or was mentioned by.
directed_graph = {nodes_list[i]['id']: links(nodes_list, i, users_count) for i in range(0, len(nodes_list))}


def directed_to_undirected(directed_graph):
    """
    Creates an undirected graph from a directed graph
    """
    for key in directed_graph.keys():
        l = directed_graph[key]
        for ngb in l:
            if key not in directed_graph[ngb]:
                directed_graph[ngb].append(key)
    return directed_graph

undirected_graph = directed_to_undirected(directed_graph)

# Plot histogram (niehgbors per node)

h = [len(undirected_graph[key]) for key in undirected_graph.keys() if len(undirected_graph[key]) < 10]
print(len(h))
plt.hist(h, bins=50)
plt.show()


def length_epsilon(lofl, n, graph):
    res = True
    for key in lofl.keys():
        if len(graph[key]) > 10 and len(lofl[key]) < n:
            res = False
            break
    return res


def graph_centrality(graph, N, users_list, verbose=False):
    graph_order = len(graph)

    # Initial node
    random_walk_loc = users_list[randint(0, graph_order - 1)]['id']

    # While the initial node is isolated (at most 1 neighbour)
    while len(graph[random_walk_loc]) < 2:
        random_walk_loc = users_list[randint(0, graph_order - 1)]['id']

    # for each node gives the last iteration we were on this node
    last_time_visited = {key: -1 for key in graph.keys()}

    # for each node gives a list of the return times to this node
    epsilon = {key: [] for key in graph.keys()}

    mu = {key: [] for key in graph.keys()}

    sigma = {key: [] for key in graph.keys()}

    iteration = 0

    while not length_epsilon(epsilon, N, graph):
        if verbose:
            print('--------------')
            print('Location of the RW : ' + str(random_walk_loc))
            print('Length of epsilon list : ' + str(len(epsilon[random_walk_loc])))

        if last_time_visited[random_walk_loc] == -1:
            # First visit to this node
            last_time_visited[random_walk_loc] = iteration
            epsilon[random_walk_loc], sigma[random_walk_loc], mu[random_walk_loc] = [], [], []

        else:
            epsilon[random_walk_loc].append(iteration - last_time_visited[random_walk_loc])
            last_time_visited[random_walk_loc] = iteration

            if len(epsilon[random_walk_loc]) > 2:
                # We add one degree of freedom (ddof=1) to get the unbiased standard error
                mu[random_walk_loc].append(np.mean(epsilon[random_walk_loc]))
                sigma[random_walk_loc].append(np.std(epsilon[random_walk_loc], ddof=1))

        # Neighbors of actual location node
        ngbs = graph[random_walk_loc]

        # Next location chosen randomly
        next_loc = ngbs[randint(0, len(ngbs) - 1)]
        d_j = len(graph[next_loc])
        d_i = len(ngbs)
        p = uniform(0, 1)

        if p <= d_i / d_j:
            # Moving onto next location
            random_walk_loc = next_loc

        iteration += 1

    return epsilon, mu, sigma

def connected(undirected_graph):
	#starting from a random nodes, return if graph is connected, explored and unexplored nodes
	unexplored_nodes = set(undirected_graph.keys())
	explored_nodes = set()
	nodes_in_exploration = [unexplored_nodes.pop()]
	explored_nodes = [nodes_in_exploration[-1]]
	i = 0
	while nodes_in_exploration != []:
		current_node = nodes_in_exploration.pop()
		for node in undirected_graph[current_node]:
			if node in unexplored_nodes and node not in nodes_in_exploration:
				nodes_in_exploration.append(node)
				unexplored_nodes.remove(node)
				explored_nodes.append(node)

	return (unexplored_nodes == set(), explored_nodes, unexplored_nodes)


def connected_components(undirected_graph):
	# returns a list of connected components of  a graph, with their size
	components = []
	unexplored_nodes = set(undirected_graph.keys())
	undirected_graph2 = undirected_graph
	while unexplored_nodes != set():
		res, explored_nodes, unexplored_nodes = connected(undirected_graph2)
		undirected_graph2 = {node : undirected_graph2[node] for node in unexplored_nodes}
		components.append((list(explored_nodes),len(explored_nodes)))
	return components

components = connected_components(undirected_graph)

print([comp[1] for comp in components], sum([comp[1] for comp in components]), len(undirected_graph))



epsilon, mu, sigma = graph_centrality(undirected_graph, 10, nodes_list, verbose = True)

l = []

for key in sigma.keys():
    if len(sigma[key]) > 10:
        l.append((key, sigma[key][-1]))

l.sort(key=lambda tup: tup[1])

print(l)
