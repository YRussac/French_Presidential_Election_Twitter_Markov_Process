# -*- coding: utf-8 -*-

import json
import datetime

with open('saved_info.txt', 'r') as f:
    l = f.read().split('\nℵ\n')
f.close()

# if JSON
dict_list = [json.loads(j) for j in l]


# List of dictionaries (one for each node/user)
nodes_list = dict_list[:-1]

# Dictionary in which the keys are the user_id and the values the number of times the user apperead while scraping
users_count = dict_list[-1]


def links(users_list, n, users_id):
    m = []
    for i in range(0, len(users_list[n]['tweets'])):
        for j in range(0, len(users_list[n]['tweets'][i]['user_mentions'])):
            if users_list[n]['tweets'][i]['user_mentions'][j] in users_id:
                #print("il a utilisé le hashtag")
                if users_list[n]['tweets'][i]['user_mentions'][j] not in m:
                    m.append(users_list[n]['tweets'][i]['user_mentions'][j])
    return m

#def link(users_list, n, users_id):
#    m=[]
#   for i in range(0, len(users_list[0]['tweets'])):
#       m = [users_list[n]['tweets'][i]['user_mentions'][j] for j in range(0, len(users_list[n]['tweets'][i]['user_mentions'])) if (users_list[n]['tweets'][i]['user_mentions'][j] not in m and users_list[n]['tweets'][i]['user_mentions'][j] in users_id)]
#    return m

g = {nodes_list[i]['id']: links(nodes_list, i, users_count) for i in range(0, len(nodes_list))}

def symetrisation(graph):
    for key in graph.keys():
        l = graph[key]
        for ngb in l:
            if key not in graph[ngb]:
                graph[ngb].append(key)
    return graph
graphe = symetrisation(g)

print(len(graphe))
print(graphe[nodes_list[600]['id']])
print("ok")
