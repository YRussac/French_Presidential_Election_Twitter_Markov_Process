import json
import numpy as np
import seaborn as sb
import os

hashtag_list = ["#Macron2017", "#Hamon2017", "#Marine2017", "#Fillon2017", "#JLM2017", "#Arthaud2017", "#Lassalle2017",
                "#Cheminade2017", "#NDA2017", "#Asselineau2017", "#Poutou2017"]

candidates_list = ['E. Macron', 'B. Hamon', 'M. Le Pen', 'F. Fillon', 'J.-L. Mélenchon', 'N. Arthaud', 'J. Lassalle',
                   'J. Cheminade', 'N. Dupont-Aignan', 'F. Asselineau', 'P. Poutou']

folders = ["seize_avril", "vingt_trois_avril_19_20", "vingt_trois_avril_21_24"]

folder = folders[0]

os.chdir(folder)

if 'Co_occurence_matrix.npy' not in os.listdir():

    with open('{}.txt'.format(folder), 'r') as lines:
        l = [line for line in lines]
    lines.close()

    dict_list = [json.loads(j) for j in l]

    # List of dictionaries (one dictionary for each node/user)
    nodes_list = dict_list[:-1]

    # Dictionary twitter_id to twitter_name
    id_to_name = {node['id']: node['screen_name'] for node in nodes_list}

    # Dictionary in which the keys are the user_id and the values the number of times the user appeared while scraping
    users_count = dict_list[-1]

    co_occurence = np.zeros((11, 11))

    for node in nodes_list:
        user_hashtags = [hashtag for tweet in node['tweets'] for hashtag in tweet['hashtags']]
        index = [i for i, hashtag in enumerate(hashtag_list) if hashtag[1:] in user_hashtags]
        for a in index:
            for b in index:
                co_occurence[a, b] += 1

    np.save('Co_occurence_matrix', co_occurence)

else:
    co_occurence = np.load('Co_occurence_matrix.npy')


sb.heatmap(co_occurence, robust=True, cmap="Blues", linewidths=.5, xticklabels=hashtag_list, yticklabels=candidates_list)
sb.plt.xticks(rotation=70)
sb.plt.yticks(rotation=0)
sb.plt.savefig('Heatmap_{}'.format(folder), dpi=400, transparent=True, bbox_inches='tight', pad_inches=0)
