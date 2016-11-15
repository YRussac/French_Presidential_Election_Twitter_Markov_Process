import creation_graphe as ini
from random import randint
from random import uniform, seed
from math import *

# For reproductivity
seed(42)

B = ini.init_graph()

def neighbors(graph, i):
    """
    This function takes the adjacency matrix of a network graph and a node as input
    Returns a list containing the nodes that a linked to the input node.
    """
    ngbs = [j for j in range(0, graph.shape[0]) if graph[i][j] == 1]
    return ngbs


def length_epsilon(lofl, n):
    res = True
    for i in range(0, len(lofl)):
        if len(lofl[i]) < n:
            res = False
            break
    return res


def sigma_i(epsilon):
    n = len(epsilon)
    sum1 = sum([epsilon[i] ** 2 for i in range(n)])
    sum2 = sum([epsilon[i] for i in range(n)])

    return sqrt(1 / n * sum1 - (1 / n * sum2) ** 2)


# the following algorithm allows me to
def second_order_centrality(graph, N):
    graph_order = graph.shape[0]

    # Initial node
    random_walk_loc = randint(0, graph_order - 1)


    # sera rempli par le temps de première viste
    visited = [-1] * graph_order

    epsilon = [[]] * graph_order

    sigma = [[]] * graph_order

    iteration = 0

    while not length_epsilon(epsilon, N):
        # print("nouvelle entrée dans la boucle")
        if visited[random_walk_loc] == -1:
            # print("je reste à l'ancienne position")
            # print(("detection d'un point jamais encore visite, première visite en t="),iteration)
            visited[random_walk_loc] = iteration
        else:

            epsilon[random_walk_loc] = epsilon[random_walk_loc] + [iteration - visited[random_walk_loc]]

            visited[random_walk_loc] = iteration
            # print("ce n'est pas ma premiere visite ici")

            if len(epsilon[random_walk_loc]) > 2:
                sigma[random_walk_loc] += [sigma_i(epsilon[random_walk_loc])]


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

        iteration += 1

    return epsilon, sigma


eps, s = second_order_centrality(B, 10000)

print(eps)
