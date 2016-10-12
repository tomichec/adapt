import numpy as np

DEBUG = 1

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt

# benchmarking
import time

from galerkin import dspl_exact

def mat_stiff(nel):
    '''constructing the global stiffness matrix'''

    # assamble local stiffness matrix (this was computed by hand)
    k = (1/dx)*np.matrix([[1,-1],[-1,1]])

    K = np.zeros((nel,nel))
    # global stiffness matrix
    for e in range(nel-1):
        K[e,e] += k[0,0]
        K[e,e+1] += k[0,1]
        K[e+1,e] += k[1,0]
        K[e+1,e+1] += k[1,1]

    K[e+1,e+1] += k[1,1]

    return K

def vec_force(nel):
    '''constructing force vector '''
    q   = -1.                         # constant of the body forces

    # local forces
    f = dx/6*np.matrix([[2,1],[1,2]])*np.matrix([[q],[q]])

    F = np.matrix(np.zeros((nel,1)))
    for e in range(nel-1):
        F[e,0] += f[0,0]
        F[e+1,0] += f[1,0]

    F[e+1,0] += f[0,0]

    return F

def sol_exact(X):
    '''returns vector of exact solution'''
    U = np.zeros((X.size))
    for i in range(X.size):
        U[i] = dspl_exact(X[i])

    return U

def eucl_norm(u,v):
    '''returns euclidian norm of vectors u and v'''
    norm = 0
    for a,b in zip(u,v):
        norm += (a-b)**2
    return np.sqrt(norm)

if __name__ == '__main__':
    
    nel = 8                           # number of elements
    L   = 1.0                         # length
    dx  = L/nel                         # space increment (uniform)
    X   = np.arange(0.0,L,dx)           # vector of position of free elements

    # Construct stiffness matrix
    print('Constructing stiffness matrix:',end='\t')
    start = time.time()
    K = mat_stiff(nel)
    print(time.time()-start)

    # Construct the force vector
    print('Constructing force vector:',end='\t')
    start = time.time()
    F = vec_force(nel)
    print(time.time()-start)        

    # find the displacement 
    print('Solving the system:',end='\t')
    start = time.time()
    # d = np.linalg.inv(K)*F    # this invert the stiffness matrix 
    d = np.linalg.solve(K,F)    # this uses LAPACK routine _gesv
    print(time.time()-start)
    
    # find the exact solution
    D = sol_exact(X)
    
    # print the results
    if DEBUG:
        print("\nStiffness matrix K:\n",K)
        print("\nForce vector F:\n",F)
        print("\nDisplacement (numerical):\n",d)
        print("\nExact displacement (computed analytically):\n",D)
        print("\nDifference between exact and numerical:\n",D-d)
        print("\nNorm of the difference:",eucl_norm(D,d))
    

    # find exact solution
    x = np.arange(0.0,L,dx/16)
    exact = dspl_exact(x)

    # plot the results
    f=plt.figure(1)
    plt.plot(x,exact,'b-')
    plt.plot(X,d,'ro-')
    plt.ylabel("displacement")
    plt.xlabel("x")
    if DEBUG:
        plt.show()
    else:
        plt.savefig('displacement1.eps', format='eps', dpi=1000)
