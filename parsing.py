# -*- coding: utf-8 -*-

import json
import datetime

with open('tiny.txt', 'r') as f:
    l = f.read().split('\nℵ\n')
f.close()

# if JSON
dict_list = [json.loads(j) for j in l]

# List of dictionaries (one for each node/user)
nodes_list = dict_list[:-1]

# Dictionary in which the keys are the user_id and the values the number of times the user apperead while scraping
users_count = dict_list[-1]

# if not JSON
#dict_list = [eval(j) for j in l]


