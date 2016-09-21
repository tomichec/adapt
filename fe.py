'''This program uses a finite element method to compute the
deformation of a hanging rod of material with a lenght L in one
dimension x. The Young modulus of E(x)=1 and cross section area A(x)=1.
'''

# import numpy as np              # TODO: consider using numpy and scipy routines which have sparse matrices routines

if __name__ == '__main__':
    # parameters of the material TODO: could be dependent on #node (position x)
    nu = 0.25                   # Young's modulus
    E = 1                       # Poisson Ratio
    h = 1                       # length of the finite element 

    L = 10                      # length of the material

    # initialize simple finite elements mesh
    invh = 1.0/h                # inverse of h 
    nel = L//h                   # number of elements (TODO: must make sure it is an integer number)
    nnodes = nel + 1             # number of nodes

    K = [[0 for x in range(nnodes)] for y in range(nnodes)] # initialise global stiffness matrix

    # X = []                      # possition of the nodes
    # con = []                    # connectivity matrix
    # for i in range(nel):
    #     X.append(i*h)           # adds location of elements
    #     con.append([i, i+1])    # linear connectivity

    # for ie in range(nel):
    #     n1 = con[ie][0]
    #     n2 = con[ie][1]
    
    # assemble stiffness matrix, TODO: make sure that the zero entries are not filled
    for i in range(nnodes):
        for j in range(i,nnodes):
            if ((j > i-2) and (j < i+2)): # affects only entries in the diagonal band
                if (j == i):
                    K[i][j] =+ 1. # ?
                if ((j < i) or (j > i)):
                    K[i][j] =+ (-1.)
                    K[j][i] =+ (-1.)
                        
    for row in K:
        for entry in row:
            print(entry,end='\t')
        print()


    

