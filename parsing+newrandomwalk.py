# -*- coding: utf-8 -*-
from random import randint
from random import uniform, seed
import numpy as np
import json
import datetime

with open('saved_info.txt', 'r') as f:
    l = f.read().split('\nℵ\n')
f.close()

# if JSON
dict_list = [json.loads(j) for j in l]
print(len(dict_list))

# List of dictionaries (one for each node/user)
nodes_list = dict_list[:-1]
print(type(nodes_list[0]['tweets'][0]['user_mentions']))

# Dictionary in which the keys are the user_id and the values the number of times the user apperead while scraping
users_count = dict_list[-1]

#for user in position n in nodes_list we get all the users of the hashtags he mentionned
def links(users_list, n, users_id):
    m = []
    for i in range(0, len(users_list[n]['tweets'])):
        for j in range(0, len(users_list[n]['tweets'][i]['user_mentions'])):
            if users_list[n]['tweets'][i]['user_mentions'][j] in users_id:
                #print("il a utilisé le hashtag")
                if users_list[n]['tweets'][i]['user_mentions'][j] not in m:
                    m.append(users_list[n]['tweets'][i]['user_mentions'][j])
    return m






g = {nodes_list[i]['id']: links(nodes_list, i, users_count) for i in range(0, len(nodes_list))}


# We symetrize the relations between mentionners and mentionned
def symetrisation(graph):
    for key in graph.keys():
        l = graph[key]
        for ngb in l:
            if key not in graph[ngb]:
                graph[ngb].append(key)
    return graph


print(len(g))


print("ok")

graphe = symetrisation(g)

print(len(graphe))

print(graphe[nodes_list[600]['id']])

#jai repris le code de yoan et modifié pour travailler sans matrice d'adjacence

#for each id returns the list of its neighboors
def neighbors(graph,id):
    """
    This function takes the adjacency matrix of a network graph and a node as input
    Returns a list containing the nodes that a linked to the input node.
    """
    ngbs = graph[id]
    return ngbs


##tests sur des noeuds qui n'ont pas bcp de voisins et qui ralentissent le code

print("noeud suspect")
n_test = neighbors(graphe, '4744709602')
n_test1 = neighbors(graphe, '14389177')
n_test2 = neighbors(graphe, '773818168032755712')

print(n_test)
print(n_test1)
print(n_test2)

print("départ de la marche")

def length_epsilon(lofl, n, graph):
    res = True
    for key in lofl.keys():
        if len(graph[key]) > 10:          #J'ai exclus les noeuds qui ont moins de 10 voisins pour le moments sinon c'est bcp trop long
            if len(lofl[key]) < n:
                print("...........")
                print(len(lofl[key]))      # pour voir quels noeuds prennent bcp de temps
                print(key)
                print("..........")
                res = False
                break
    return res


def graph_centrality(graph, N, users_list):
    graph_order = len(graph) # au lieu de graph.shape utilisé précédement


    # Initial node


    rand_int = randint(0, graph_order - 1)
    random_walk_loc = users_list[rand_int]['id']        # au lieu de :  random_walk_loc = randint(0, graph_order - 1)

    print(random_walk_loc)


    while len(graph[random_walk_loc]) < 2:
         print("j'ai pas d'amis")
         rand_int = randint(0, graph_order - 1)
         random_walk_loc = users_list[rand_int]['id']
         print(random_walk_loc)

    # sera rempli par le temps de première viste

    last_time_visited = {key: -1 for key in graph.keys()} # au lieu de last_time_visited = [-1] * graph_order # A changer
    print(last_time_visited[random_walk_loc])


    epsilon = {key: [] for key in graph.keys()}         # au lieu de epsilon = [[]] * graph_order

    #mu = [[]] * graph_order
    mu = {key: [] for key in graph.keys()}

    #sigma = [[]] * graph_order
    sigma = {key: [] for key in graph.keys()}

    iteration = 0

    same_loc = False

    while not length_epsilon(epsilon, N, graph):

        print("__________________")
        print("position dans le graphe")
        print(random_walk_loc)

        if last_time_visited[random_walk_loc] == -1:
            # print("je reste à l'ancienne position")
            #  print(("detection d'un point jamais encore visite, première visite en t="),iteration)
            last_time_visited[random_walk_loc] = iteration
            epsilon[random_walk_loc], sigma[random_walk_loc], mu[random_walk_loc] = [], [], []

        else:
            epsilon[random_walk_loc].append(iteration - last_time_visited[random_walk_loc])
            print("longueur de epsilon au noeud")
            print(random_walk_loc)
            print(len(epsilon[random_walk_loc]))    # pour voir ou on en est pour chaque noeud
            last_time_visited[random_walk_loc] = iteration
            #print("ce n'est pas ma premiere visite ici")

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
        p = uniform(0, 1)

        if p <= d_i / d_j:
            # Moving onto next location
            random_walk_loc = next_loc

        iteration += 1
        print(iteration)


    return epsilon, mu, sigma

rd = graph_centrality(graphe, 10, nodes_list)

print("FIN de la marche")
print(rd[2])

