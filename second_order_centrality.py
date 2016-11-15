import creation_graphe as ini
from random import randint
from random import uniform
from math import *

B = ini.init_graph()


def neighbors(graph, i):
    """
    This function takes the adjacency matrix of a network graph and a node as input
    Returns a list containing the nodes that a linked to the input node.
    """
    res = [j for j in range(0, graph.shape[0]) if graph[i][j] == 1]
    return res


def length_epsilon(lofl, n):
    res = True
    for i in range(0, len(lofl)):
        if len(lofl[i]) < n:
            res = False
            break
    return res


def sigma_i(l, n):
    sum1 = sum([l[i] ** 2 for i in range(n)])
    sum2 = sum([l[i] for i in range(n)])

    return sqrt(1 / n * sum1 - (1 / n * sum2) ** 2)


# the following algorithm allows me to
def second_order_centrality(graph, N):
    graph_order = graph.shape[0]

    # Initial node
    random_walk_loc = randint(0, graph_order - 1)

    visited = [-1] * graph_order

    epsilon = [[]] * graph_order

    sigma = [[]] * graph_order

    iteration = 0

    cont = True

    while length_epsilon(epsilon, N) == False:
        # print("nouvelle entrée dans la boucle")
        iteration += 1

        if visited[random_walk_loc] == -1:
            # print("je reste à l'ancienne position")
            # print(("detection d'un point jamais encore visite, première visite en t="),iteration)
            visited[random_walk_loc] = iteration
        else:
            # how many times did we visit the vertice n°i
            epsilon[random_walk_loc] += [iteration - visited[random_walk_loc]]
            # print("ce n'est pas ma premiere visite ici")

            if len(epsilon[random_walk_loc]) > 3:
                sigma[random_walk_loc] = [sigma_i(epsilon[random_walk_loc], len(epsilon[random_walk_loc]))]


            # Neighbors of actual location node
        ngbs = neighbors(graph, random_walk_loc)

        # Next location chosen randomly
        next_loc = ngbs[randint(0, len(ngbs) - 1)]

        d_j = len(neighbors(graph, next_loc))
        d_i = len(ngbs)
        p = uniform(0, 1)

        if p <= d_i / d_j:
            # Moving onto next location
            random_walk_loc = next_loc
        else:
            # Staying on actual location
            pass


    return epsilon, sigma


print(second_order_centrality(B, 4))




