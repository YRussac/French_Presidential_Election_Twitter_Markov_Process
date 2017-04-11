# This file contains the functions we use to construct and work on graphs

from random import randint
from random import uniform, seed
import sys
import numpy as np
import json
import datetime
import matplotlib.pyplot as plt


def links(users_list, n, users_id):
    """
    for user in position n in nodes_list we get all the users of the hashtags he mentionned
    """
    m = []
    # On parcourt les tweets d'un user n donné
    for i in range(0, len(users_list[n]['tweets'])):

        # Pour chaque tweet on parcourt les utilisateurs mentionnes
        for j in range(0, len(users_list[n]['tweets'][i]['user_mentions'])):

            # si un utilisateur mentionné est dans la liste qui contient tous les users qui ont utilisé un des hashtags
            if users_list[n]['tweets'][i]['user_mentions'][j] in users_id:
                if users_list[n]['tweets'][i]['user_mentions'][j] not in m and users_list[n]['tweets'][i]['user_mentions'][j] != users_list[n]['id']:
                    m.append(users_list[n]['tweets'][i]['user_mentions'][j])
    return m


def directed_to_undirected(directed_graph):
    """
    Creates an undirected graph from a directed graph
    """
    for key in directed_graph.keys():
        l = directed_graph[key]
        for ngb in l:
            if key not in directed_graph[ngb]:
                directed_graph[ngb].append(key)
    return directed_graph


def connected(undirected_graph):
    #starting from a random nodes, return if graph is connected, explored and unexplored nodes
    unexplored_nodes = set(undirected_graph.keys())
    explored_nodes = set()
    nodes_in_exploration = [unexplored_nodes.pop()]
    explored_nodes = [nodes_in_exploration[-1]]
    i = 0
    while nodes_in_exploration != []:
        current_node = nodes_in_exploration.pop()
        for node in undirected_graph[current_node]:
            if node in unexplored_nodes and node not in nodes_in_exploration:
                nodes_in_exploration.append(node)
                unexplored_nodes.remove(node)
                explored_nodes.append(node)
    return unexplored_nodes == set(), explored_nodes, unexplored_nodes


# returns a list of connected components of  a graph, with their size
def connected_components(undirected_graph):
    components = []
    unexplored_nodes = set(undirected_graph.keys())
    undirected_graph2 = undirected_graph
    while unexplored_nodes != set():
        res, explored_nodes, unexplored_nodes = connected(undirected_graph2)
        undirected_graph2 = {node : undirected_graph2[node] for node in unexplored_nodes}
        components.append((list(explored_nodes),len(explored_nodes)))
    return components

#returns a dictionnary where the keys are the 'id' and for each 'id' we have the hashtags he used and the number of times he used it
#def users_hashtag(i, hashtag_list):
def users_hashtag(i):    
    l = {}
    for tweets in nodes_list[i]['tweets']:
        if (tweets['hashtags'] != []):
            for hashtags in tweets['hashtags']:
                #if hashtags in hashtag_list:                #If we only want hashatgs from the track list used for scrapping
                if hashtags in l:
                    l[hashtags] += 1
                else:
                    l[hashtags] = 1
    return l
NbHashtags_used = {nodes_list[i]['id']: users_hashtag(i) for i in range(0, len(nodes_list))}

