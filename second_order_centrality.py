import creation_graphe as ini
from random import randint
from random import uniform
from math import *

B = ini.init_graph()

def neighbor(graph,i):
    """
    This function takes the adjacency matrix of a network graph and a node as input
    Returns a list containing the nodes that a linked to the input node.
    """
    res = [j for j in range(0,graph.shape[0]) if graphe[i][j]==1]
    return res

def length_epsilon(lofl,N):
    n = len(lofl)
    res = True
    for i in range(0,n):
        if len(lofl[i]) < N:
            cont = False
            res = False
    return res

def sigma_i(l,n):
    sum1 = sum([l[i]**2 for i in range(n)])
    sum2 = sum([l[i] for i in range(n)])
    
    return sqrt(1/(n)*sum1-(1/(n)*sum2)**2)


# the following algorithm allows me to
def second_order_centrality(graphe,N):
    graph_order = graphe.shape[0]
    random_walk_loc = randint(0,graph_order-1)
    #print((" Noeud initial"),random_walk_pos)

    visited = [-1]*graph_order
    epsilon = [[]]*graph_order
    sigma = [[]]*graph_order
    iter = 0
    cont = True
    while cont==True:

        if length_epsilon(epsilon,N)==True:
            cont = False
            #print(iter)
            #print(("first time in this vertice"),visited)
        else:
            iter += 1
            #print("----- nouvelle entrée dans la boucle")
            surrounding=neighbor(graphe,random_walk_loc)
            #print(("je suis situé en"),random_walk_pos)
            #print("")
            #print(("les voisins sont "),surrounding)
            next_loc = surrounding[randint(0,len(surrounding)-1)]
            d_j = len(neighbor(graphe,next_loc))
            d_i = len(surrounding)
            p = uniform(0,1)
            if p<=d_i/d_j:
                #print(("deplacement vers",next_pos))
                random_walk_loc=next_loc
            else:
                pass

            if visited[random_walk_loc]==-1:
                #print("je reste à l'ancienne position")
                #print(("detection d'un point jamais encore visite, première visite en t="),iter)
                visited[random_walk_loc]=iter
            else:
                # how many times did we visit the vertice n°i
                epsilon[random_walk_loc] += [iter-visited[random_walk_loc]]
                #print("ce n'est pas ma première visite ici")
                #print(("voici les temps de retour calculés"),epsilon[random_walk_pos])
                if len(epsilon[random_walk_loc])>3:
                    sigma[random_walk_loc] += [sigma_i(epsilon[random_walk_loc],len(epsilon[random_walk_loc]))]

    return epsilon,sigma





print(second_order_centrality(B,3))








