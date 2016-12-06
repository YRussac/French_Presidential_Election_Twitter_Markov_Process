
from random import randint
from random import uniform, seed
import numpy as np


def neighbors(graph, i):
    """
    This function takes the adjacency matrix of a network graph and a node as input
    Returns a list containing the nodes that a linked to the input node.

    """
    ngbs = [j for j in range(0, graph.shape[0]) if graph[i][j] == 1]
    return ngbs


def length_list_of_list(list_of_list, n):
    """
    This function takes a list of lists as an input
    Returns a bool, the result will be true if and only if the size of each of lists is greater or
    equal than n the second parameter
    """
    res = True
    for i in range(0, len(list_of_list)):
        if len(list_of_list[i]) < n:
            res = False
            break
    return res


def graph_centrality(graph, N):
    """
    This function take the adjency matrix of a graph and a size N as input.
    N is linked with the minimum number of times we want to return to every single vertices
    For example if N=10 at the end of the algorithm, we will have at least 10 return times for each vertice
    """
    graph_order = graph.shape[0]

    # Initial node
    random_walk_loc = randint(0, graph_order - 1)  # we randomly choose the vertice where the random walk starts

    # will be filled with the first visit time
    last_time_visited = [-1] * graph_order

    epsilon = [[]] * graph_order

    mu = [[]] * graph_order

    sigma = [[]] * graph_order

    iteration = 0

    same_loc = False

    while not length_list_of_list(epsilon, N): # we must have at least N times of return for each vertices
        if not same_loc:

            if last_time_visited[random_walk_loc] == -1:  # first time we visit this specific node

                # print(("detection of an unvisited point, first visit for t="),iteration)
                last_time_visited[random_walk_loc] = iteration
                epsilon[random_walk_loc], sigma[random_walk_loc], mu[random_walk_loc] = [], [], []

            else:
                epsilon[random_walk_loc].append(iteration - last_time_visited[random_walk_loc])
                # we had the new return time to the list for the node where we currently are
                last_time_visited[random_walk_loc] = iteration
                # print("Not our first visit on this vertice")

                if len(epsilon[random_walk_loc]) > 2:
                    # We add one degree of freedom (ddof=1) to get the unbiased standard error
                    mu[random_walk_loc].append(np.mean(epsilon[random_walk_loc]))
                    sigma[random_walk_loc].append(np.std(epsilon[random_walk_loc], ddof=1))

        # Neighbors of actual location node
        ngbs = neighbors(graph, random_walk_loc)

        # Next location chosen randomly
        next_loc = ngbs[randint(0, len(ngbs) - 1)]

        d_j = len(neighbors(graph, next_loc))
        d_i = len(ngbs)
        # d_i is the degree of the current vertice
        # d_j is the degree of the eventual following vertice for our random walk
        p = uniform(0, 1)

        if p <= d_i / d_j:
            # Moving onto next location
            random_walk_loc = next_loc
            same_loc = False
        else:
            same_loc = False
            #same_loc = True

        iteration += 1

    return epsilon, mu, sigma


def transition_mat(adjacency_matrix):
    graph_degree = adjacency_matrix.shape[0]
    transition_matrix = np.zeros((graph_degree, graph_degree))

    for i in range(graph_degree):
        # degree of node i
        d_i = sum(adjacency_matrix[i])
        prob = 0
        for j in range(graph_degree):
            # if j is a neighbour of i then we compute its degree
            if adjacency_matrix[i][j] == 1:
                d_j = sum(adjacency_matrix[j])

                # Proba(to pass in j/knowing we are in i)= (1/di)*min(1,di/dj)
                if d_i >= d_j and d_i != 0:
                    transition_matrix[i][j] = 1 / d_i
                    prob += transition_matrix[i][j]
                else:
                    transition_matrix[i][j] = 1 / d_j
                    prob += transition_matrix[i][j]
            transition_matrix[i][i] = 1 - prob
            # probability of staying in i

    return transition_matrix


def theoretical_second_order_centrality(transition_matrix):
    sigma = []

    graph_degree = transition_matrix.shape[0]

    for j in range(graph_degree):
        Q = transition_matrix.copy()

        for i in range(graph_degree):
            # Q(i,l)= 0 if l=j P(i,l) otherwise
            Q[i][j] = 0

        # M=inv(Id-Q)
        M = np.linalg.inv(np.eye(graph_degree) - Q)

        # Mj = M*vector(1)
        M_j = np.dot(M, np.transpose(np.ones(graph_degree)))

        # we compute sigma for each node
        sigma_j = np.sqrt(2 * sum(M_j) - graph_degree * (graph_degree + 1))
        sigma.append(sigma_j)

    return sigma