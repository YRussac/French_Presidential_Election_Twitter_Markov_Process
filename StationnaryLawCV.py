# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:25:35 2017

@author: LTINSI
"""
import seaborn
import matplotlib.pyplot as plt
import os
#print(os.getcwd())
import xlrd
centralite = xlrd.open_workbook('/Users/lauratinsi/Desktop/ENSAE/2A/Statapp_graphe/excel/Centralite_seize_avril.xlsx')
print (centralite.sheet_names())
sh = centralite.sheet_by_name(u'Sheet1')
colonne = sh.col_values(2)[1:]

print(colonne)
l = []
for i in range (0, len(colonne)+50):
    l.append(13327)
fig = plt.figure()


ax = fig.add_subplot(111)
ax.plot(l,'palevioletred')
ax.plot(colonne, color = 'lightcoral')

plt.title('Return times empiric means of the nodes for the graph of April,16')
plt.ylabel('Empiric mean')
plt.xlabel('Nodes ordered increasingly according to their return times empiric mean')

plt.show()