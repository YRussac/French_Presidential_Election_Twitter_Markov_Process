from random import randint
from random import uniform, seed
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# Zakary's Karate Club Graph
G = nx.karate_club_graph()
B = nx.adjacency_matrix(G).toarray()

# For reproducibility
seed(42)

plot = True

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

# the following algorithm allows me to
def second_order_centrality(graph, N):
    graph_order = graph.shape[0]

    # Initial node
    random_walk_loc = randint(0, graph_order - 1)

    # sera rempli par le temps de première viste
    visited = [-1] * graph_order

    epsilon = [[]] * graph_order

    mu = [[]] * graph_order

    sigma = [[]] * graph_order

    iteration = 0

    same_loc = False

    while not length_epsilon(epsilon, N):
        if not same_loc:
            # print("Nouvelle entrée dans la boucle")
            if visited[random_walk_loc] == -1:
                # print("je reste à l'ancienne position")
                # print(("detection d'un point jamais encore visite, première visite en t="),iteration)
                visited[random_walk_loc] = iteration
            else:
                epsilon[random_walk_loc] = epsilon[random_walk_loc] + [iteration - visited[random_walk_loc]]
                visited[random_walk_loc] = iteration
                # print("ce n'est pas ma premiere visite ici")

                if len(epsilon[random_walk_loc]) > 2:
                    # We add one degree of freedom (ddof=1) to get the unbiased standard error
                    sigma[random_walk_loc] = sigma[random_walk_loc] + [np.std(epsilon[random_walk_loc], ddof=1)]
                    mu[random_walk_loc] = mu[random_walk_loc] + [np.mean(epsilon[random_walk_loc])]

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
            same_loc = False
        else:
            same_loc = True

        iteration += 1

    return epsilon, mu, sigma


n = 500

eps, m, s = second_order_centrality(B, n)

colors_m = [l[-1] for l in m]
colors_s = [l[-1] for l in s]

#nx.draw_networkx(G, node_color=colors_m, alpha=0.5, cmap=plt.get_cmap('bwr'))
nx.draw_networkx(G, node_color=colors_s, alpha=0.5, cmap=plt.get_cmap('bwr'))


if plot:
    x = [i for i in range(n-2)]

    plt.subplots(nrows=5, ncols=2, sharex=True, figsize=(6, 6))

    print('Plotting')

    for i in range(10):
        ax = plt.subplot(5, 2, i + 1)
        ax.yaxis.tick_right()
        ax.title.set_text('Centralité de second ordre du noeud {}'.format(i))
        ax.plot(x, s[i][:n - 2])

    plt.tight_layout()
    plt.show()




