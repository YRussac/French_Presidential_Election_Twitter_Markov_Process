# This file contains the functions we use to compute nodes centralities

from random import randint
from random import uniform
import datetime


def pathological_nodes_search(epsilon):
    """
    Function to detect nodes that have less than 10 non-consecutives returns
    """
    nodes_to_delete = []
    for key in epsilon.keys():
        i = 0
        for j in range(0, len(epsilon[key])):
                if epsilon[key][j] != 1:
                    i += 1
                if i == 9:
                    break
        if i < 9:
            nodes_to_delete.append(key)
    return nodes_to_delete


def graph_centrality(graph, n, verbose=False, method="M", d=0.85):
    """"
    Method is M for Metropolis and P for PageRank, d is a PageRank algorithm parameter (which one ?)
    """
    graph_order = len(graph)

    nodes = list(graph.keys())
    # Initial node
    random_walk_loc = nodes[randint(0, graph_order - 1)]

    # While the initial node is isolated (at most 1 neighbour)
    while len(graph[random_walk_loc]) < 2:
        random_walk_loc = nodes[randint(0, graph_order - 1)]

    # Gives for each node the last iteration we were on this node
    last_time_visited = {node: -1 for node in graph.keys()}

    # For each node gives a list of the return times to this node
    epsilon = {node: [] for node in graph.keys()}

    iteration = 0

    number_of_return_times = {node: 0 for node in graph.keys() if len(graph[node]) > 10}

    while bool(number_of_return_times):
        if verbose:
            print('--------------')
            print('Location of the RW : ' + str(random_walk_loc))
            print('Length of epsilon list : ' + str(len(epsilon[random_walk_loc])))

        if last_time_visited[random_walk_loc] == -1:
            # First visit to this node
            last_time_visited[random_walk_loc] = iteration
            epsilon[random_walk_loc] = []

        else:
            epsilon[random_walk_loc] = epsilon[random_walk_loc][-1500:] + [(iteration - last_time_visited[random_walk_loc])]
            last_time_visited[random_walk_loc] = iteration

        if random_walk_loc in number_of_return_times.keys():
            number_of_return_times[random_walk_loc] += 1
            if number_of_return_times[random_walk_loc] == 1500:
                number_of_return_times.pop(random_walk_loc)

        # Neighbors of actual location node
        neighbors = graph[random_walk_loc]

        if method == "M":
            # Next location chosen randomly
            next_location = neighbors[randint(0, len(neighbors) - 1)]
            d_j = len(graph[next_location])
            d_i = len(neighbors)
            p = uniform(0, 1)

            if p <= d_i / d_j:
                # Moving onto next location
                random_walk_loc = next_location

        elif method == "P":
            p = uniform(0, 1)
            if len(neighbors) == 0 or p < 1 - d:
                random_walk_loc = nodes[randint(0, graph_order - 1)]
            else:
                random_walk_loc = neighbors[randint(0, len(neighbors) - 1)]
        else:
            return "Parameter method should be 'M' for Metropolis-Hastings or 'P' for PageRank"

        iteration += 1
        
    pathological_nodes = pathological_nodes_search(epsilon)
    return epsilon, pathological_nodes, number_of_return_times
