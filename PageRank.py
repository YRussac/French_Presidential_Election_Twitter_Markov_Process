import numpy as np

def PR_transition_matrix(graph, d):
    A = np.ones((len(graph), len(graph))) * (1-d)/len(graph) #probability of teleportation
    Sorted_nodes = {} #define nodes order
    i = 0
    for node in graph:
        if node not in Sorted_nodes:
            Sorted_nodes[node] = i
            i+=1
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
    x1 /= np.linalg.norm(x1)
    x2 = np.dot(x1, A)
    while np.linalg.norm(x2 - x1) > epsilon:
        x1 = x2.copy()
        x2 = np.dot(x1, A) / np.linalg.norm(x1)
    return x2

if __name__ == "__main__":
    #test

    graph = {1 : [2, 3], 2 : [3], 3 : [1]}
    print(graph)
    A = PR_transition_matrix(graph, 1)
    print(A)

    print(Page_Rank(graph, 0.85, 0.00001))