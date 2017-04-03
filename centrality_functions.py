# This file contains the functions we use to compute nodes centralities

from random import randint
from random import uniform, seed
import numpy as np
import datetime


def length_epsilon(lofl, n, graph):
    for key in lofl.keys():
        if len(graph[key]) > 10 and len(lofl[key]) < n:
            return False
    return True


def graph_centrality(graph, N, verbose=False):

    graph_order = len(graph)

    nodes = list(graph.keys())
    # Initial node
    random_walk_loc = nodes[randint(0, graph_order - 1)]

    # While the initial node is isolated (at most 1 neighbour)
    while len(graph[random_walk_loc]) < 2:
        random_walk_loc = nodes[randint(0, graph_order - 1)]

    # for each node gives the last iteration we were on this node
    last_time_visited = {key: -1 for key in graph.keys()}

    # for each node gives a list of the return times to this node
    epsilon = {key: [] for key in graph.keys()}

    # mu = {key: [] for key in graph.keys()}

    # sigma = {key: [] for key in graph.keys()}

    iteration = 0

    while not length_epsilon(epsilon, N, graph):
        if verbose:
            print('--------------')
            print('Location of the RW : ' + str(random_walk_loc))
            print('Length of epsilon list : ' + str(len(epsilon[random_walk_loc])))

        if last_time_visited[random_walk_loc] == -1:
            # First visit to this node
            last_time_visited[random_walk_loc] = iteration
            epsilon[random_walk_loc] = []
            # sigma[random_walk_loc], mu[random_walk_loc] = [], [], []

        else:
            epsilon[random_walk_loc].append(iteration - last_time_visited[random_walk_loc])
            last_time_visited[random_walk_loc] = iteration

            # if len(epsilon[random_walk_loc]) > 2:
                # We add one degree of freedom (ddof=1) to get the unbiased standard error
                # mu[random_walk_loc].append(np.mean(epsilon[random_walk_loc]))
                # sigma[random_walk_loc].append(np.std(epsilon[random_walk_loc], ddof=1))

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

    return epsilon
    #return epsilon, mu, sigma
