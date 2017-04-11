import numpy as np
from centrality_functions import graph_centrality

def PR_transition_matrix(graph, d):
    A = np.ones((len(graph), len(graph))) * (1-d)/len(graph) #probability of teleportation
    Sorted_nodes = {} #define nodes order
    i = 0
    for node in graph:
        if node not in Sorted_nodes:
            Sorted_nodes[node] = i
            i+=1
        if graph[node] == []:
            A[Sorted_nodes[node] , : ] += d/len(graph)
        for neighbour_node in graph[node]:
            if neighbour_node not in Sorted_nodes:
                Sorted_nodes[neighbour_node] = i
                i+=1
            A[Sorted_nodes[node], Sorted_nodes[neighbour_node]] += d*1/len(graph[node]) #uniform probability
    return A



def Page_Rank(graph, d, epsilon):
    #calculate the eigenvector of for the eigenvalue = 1
    A = PR_transition_matrix(graph, d)
    x1 = np.ones((1, len(graph)))
    x2 = np.dot(x1, A)
    x2 /= np.linalg.norm(x2, ord = 1, axis = 1)
    while np.linalg.norm(x2 - x1) > epsilon:
        x1 = x2.copy()

        x2 = np.dot(x1, A)
        x2 /= np.linalg.norm(x2, ord = 1, axis = 1)
    return x2


if __name__ == "__main__":
    #test

    graph = {1 : [2, 3, 4], 2 : [3, 4], 3 : [1, 4], 4 : []}
    print(graph)
    A = PR_transition_matrix(graph, 0.85)
    print(A)

    print(Page_Rank(graph, 0.85, 0.0000001))
    epsilon = graph_centrality(graph, 5000, method = "P")
    print("stochastic :")
    for key in epsilon:
        print(key, " ", len(epsilon[key])/sum(epsilon[key])) # to make that test work change len(graph[key]) > 10 to >1
                                                             # in length_epsilon in centrality_functions.py