import creation_graphe as ini
from random import randint
from random import uniform
from math import *

B = ini.init_graph()

def neighbor(graphe,i):
    res = [j for j in range(0,len(graphe[0])) if graphe[i][j]==1]
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
    card_vertices = len(graphe[0])
    random_walk_pos = randint(0,card_vertices-1)
    #print((" Noeud initial"),random_walk_pos)

    visited = [-1]*card_vertices
    epsilon = [[]]*card_vertices
    sigma = [[]]*card_vertices
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
            surrounding=neig(graphe,random_walk_pos)
            #print(("je suis situé en"),random_walk_pos)
            #print("")
            #print(("les voisins sont "),surrounding)
            next_pos = surrounding[randint(0,len(surrounding)-1)]
            d_j = len(neighbor(graphe,next_pos))
            d_i = len(surrounding)
            p = uniform(0,1)
            if p<=d_i/d_j:
                #print(("deplacement vers",next_pos))
                random_walk_pos=next_pos
            else:
                pass

            if visited[random_walk_pos]==-1:
                #print("je reste à l'ancienne position")
                #print(("detection d'un point jamais encore visite, première visite en t="),iter)
                visited[random_walk_pos]=iter
            else:
                # how many times did we visit the vertice n°i
                epsilon[random_walk_pos]=epsilon[random_walk_pos]+[iter-visited[random_walk_pos]]
                #print("ce n'est pas ma première visite ici")
                #print(("voici les temps de retour calculés"),epsilon[random_walk_pos])
                if len(epsilon[random_walk_pos])>3:
                    sigma[random_walk_pos]=sigma[random_walk_pos]+[sigma_i(epsilon[random_walk_pos],len(epsilon[random_walk_pos]))]

    return((epsilon),sigma)





print(second_order_centrality(B,3))








