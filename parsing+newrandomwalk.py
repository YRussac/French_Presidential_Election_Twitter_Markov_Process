# -*- coding: utf-8 -*-
from random import randint
from random import uniform, seed
import numpy as np
import json
import datetime

# Parsing
with open('saved_info.txt', 'r') as f:
    l = f.read().split('\nℵ\n')
f.close()

dict_list = [json.loads(j) for j in l]

# List of dictionaries (one for each node/user)
nodes_list = dict_list[:-1]

# Dictionary in which the keys are the user_id and the values the number of times the user appeared while scraping
users_count = dict_list[-1]


# for user in position n in nodes_list we get all the users of the hashtags he mentionned
def links(users_list, n, users_id):
    """
    :param users_list:
    :param n: position of the user of interest in the users_list
    :param users_id:
    :return:
    """
    m = []
    # On parcourt les tweets d'un user n donné
    for i in range(0, len(users_list[n]['tweets'])):

        # Pour chaque tweet on parcourt les utilisateurs mentionnes
        for j in range(0, len(users_list[n]['tweets'][i]['user_mentions'])):

            # si un utilisateur mentionné est dans la liste qui contient tous les users qui ont utilisé un des hashtags
            if users_list[n]['tweets'][i]['user_mentions'][j] in users_id:

                if users_list[n]['tweets'][i]['user_mentions'][j] not in m:
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


def length_epsilon(lofl, n, graph):
    res = True
    for key in lofl.keys():
        if len(graph[key]) > 10 and len(lofl[key]) < n:
            res = False
            break
    return res


def graph_centrality(graph, N, users_list):

    graph_order = len(graph)

    # Initial node
    random_walk_loc = users_list[randint(0, graph_order - 1)]['id']

    # While the initial node is isolated (at most 1 neighbour)
    while len(graph[random_walk_loc]) < 2:
        random_walk_loc = users_list[randint(0, graph_order - 1)]['id']
    print(random_walk_loc)

    # for each node gives the last iteration we were on this node
    last_time_visited = {key: -1 for key in graph.keys()}

    # for each node gives a list of the return times to this node
    epsilon = {key: [] for key in graph.keys()}

    mu = {key: [] for key in graph.keys()}

    sigma = {key: [] for key in graph.keys()}

    iteration = 0

    while not length_epsilon(epsilon, N, graph):
        print('--------------')
        print('Location of the RW : ' + str(random_walk_loc))
        print('Length of epsilon list : ' + str(len(epsilon[random_walk_loc])))

        if last_time_visited[random_walk_loc] == -1:
            print('First visit')
            last_time_visited[random_walk_loc] = iteration
            epsilon[random_walk_loc], sigma[random_walk_loc], mu[random_walk_loc] = [], [], []
        else:
            print('Multiple visits')
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

rd = graph_centrality(undirected_graph, 10, nodes_list)



