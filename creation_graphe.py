import numpy as np

## fonction to create the graph
def sym(A,n):
    for i in range(0,n):
        for j in range(i+1,n):
            if A[i][j]!=0:
                A[j][i]=A[i][j]
    return(A)

def init_graph():
    B=np.zeros((10,10))
    # 0 vertice
    B[0][9]=1
    # vertice number 1

    B[1][2]=1
    B[1][4]=1
    B[1][5]=1
    # vertice number 2
    B[2][3]=1
    B[2][4]=1
    # vertice number 3
    B[3][4]=1
    B[3][7]=1
    # vertice number 4
    B[4][5]=1
    # vertice number 5
    B[5][6]=1
    # vertice number 7
    B[7][8]=1
    # vertice number 8
    B[8][9]=1
    return(sym(B,10))



