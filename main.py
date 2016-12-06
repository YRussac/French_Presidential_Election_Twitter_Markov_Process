import matplotlib.pyplot as plt
import networkx as nx
from functions import *

# We load Zakary's Karate Club Graph
G = nx.karate_club_graph()
B = nx.adjacency_matrix(G).toarray()

tm = transition_mat(B)
theoretical_values = theoretical_second_order_centrality(tm)

# For reproducibility
seed(42)

plot = True
n = 2000

# We compute the first and second order centrality for the graph we loaded
eps, m, s = graph_centrality(B, n)

colors_m = [l[-1] for l in m]
colors_s = [l[-1] for l in s]

# nx.draw_networkx(G, node_color=colors_m, alpha=0.5, cmap=plt.get_cmap('bwr'))
nx.draw_networkx(G, node_color=colors_s, alpha=0.5, cmap=plt.get_cmap('bwr'))


if plot:
    x = [i for i in range(n-2)]

    plt.subplots(nrows=5, ncols=3, sharex=True, figsize=(6, 6))

    print('Plotting')

    for i in range(15):
        ax = plt.subplot(5, 3, i + 1)
        ax.yaxis.tick_right()
        ax.title.set_text('Node {} 2nd order centrality'.format(i))
        ax.plot(x, s[i][:n - 2])
        ax.axhline(y=theoretical_values[i], c="red", linewidth=3, zorder=0)

    plt.tight_layout()
    plt.show()
