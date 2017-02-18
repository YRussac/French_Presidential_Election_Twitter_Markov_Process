import json
import datetime

with open('saved_info.txt', 'r') as f:
    l = f.read().split('ℵ')
f.close()

# if JSON
# dict_list = [json.loads(j) for j in l]

# if not JSON
dict_list = [eval(j) for j in l]


