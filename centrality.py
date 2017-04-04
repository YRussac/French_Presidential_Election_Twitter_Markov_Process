import json
import numpy as np
import matplotlib.pyplot as plt

with open('epsilon.json', 'r') as f:
    epsilon = json.load(f)
f.close()

mu = {}
sigma = {}


for node in epsilon:
    mu[node] = np.mean(epsilon[node])
    sigma[node] = np.std(epsilon[node], ddof=1)

l = [(key, sigma[key]) for key in sigma.keys() if len(epsilon[key]) > 500]
l.sort(key=lambda tup: tup[1])
print(l)

l = [(key, mu[key]) for key in sigma.keys() if len(epsilon[key]) > 500]
l.sort(key=lambda tup: tup[1])
print(l)


for key in epsilon.keys():
    if len(epsilon[key]) > 500:
        s = [np.std(epsilon[key][100:i], ddof=1) for i in range(100, len(epsilon[key]))]
        plt.plot(s)
        plt.show()