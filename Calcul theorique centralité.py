# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 09:48:33 2016

@author: lauratinsi
"""

import numpy as np 
import math as mt

A=[[1/2, 0, 0, 0, 0, 0, 0, 0, 0, 1/2],[0, 1/12, 1/3, 0, 1/4, 1/3, 0, 0, 0, 0],
   [0, 1/3, 1/12, 1/3, 1/4, 0, 0, 0, 0, 0],[0, 0, 1/3, 1/12, 1/4, 0, 0, 1/3, 0, 0],
[0, 1/4, 1/4, 1/4, 0, 1/4, 0, 0, 0, 0],[0, 1/3, 0, 0, 1/4, 1/12, 1/3, 0, 0, 0],
[0, 0, 0, 0, 0, 1/3, 2/3, 0, 0, 0],[0, 0, 0, 1/3, 0, 0, 0, 1/6, 1/2, 0],
[0, 0, 0, 0, 0, 0, 0, 1/2, 0, 1/2],[1/2, 0, 0, 0, 0, 0, 0, 0, 1/2, 0]];

def transition_mat(adj):
    
    P=np.array(len(adj),len(adj)) #P transition matrice
    
    for i in range (0, len(adj)): 
        
        d_i=sum(adj[i])   # i node's degree
        
        prob=0
        
        for j in range (0, len(adj)):
            
            if (adj[i][j]==1):   #if j is a neighbourgh of i then we compute its degree
                
                d_j=sum(adj[j])
                
                if (d_i>=d_j and d_i!=0)  : #Proba(to pass in j/knowing we are in i)= (1/di)*min(1,di/dj)
                    
                    P[i][j]= 1/d_i
                    
                    prob+=P[i][j]
                    
                else : 
                    P[i][j]=1/d_j
                    
                    prob+=P[i][j]
                
                
            P[i][i]=1-prob # probability to stay in i
    
    return P
                    

def cal_theo(A):
    
    L=[]
    
    for j in range(0,len(A)):
        
           Q= np.array([[A[l][m] for l in range(0,len(A))] for m in range(0,len(A))])

           for i in range(0, len(A)):
               
                   Q[i][j]= 0           #Q(i,l)= 0 if l=j P(i,l) otherwise
                   
           M =np.linalg.inv(np.eye(len(A))+np.dot(-1*np.eye(len(A)),Q))  # M=inv(Id-Q)
           
           M_j=np.dot(M, np.transpose(np.ones(len(A))))     #Mj=M*vector(1)
           
           sig_j=mt.sqrt(2*sum(M_j)-len(A)*(len(A)+1))      # we compute sigma for each node
           
           L.append(sig_j)
           
    return L
       
print(cal_theo(A))

            
            
        
    