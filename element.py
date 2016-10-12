import numpy as np

DEBUG = 1

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt

def dspl_exact(x,q=-1):
    '''exact displacement for our problem'''
    return q/2 *(1-x**2)

def forces(x):
    '''return constant body forces'''
    q   = -1
    return q

def mat_stiff(X):
    '''constructing the global stiffness matrix'''

    K = np.zeros((nel,nel))
    # global stiffness matrix
    for e in range(X.size-1):
        # length of the element
        dx = X[e+1] - X[e]     # assamble local stiffness matrix (this was computed by hand)
        # assamble local stiffness matrix (this was computed by hand)
        k = (1/dx)*np.array([[1,-1],[-1,1]])

        K[e,e] += k[0,0]
        K[e,e+1] += k[0,1]
        K[e+1,e] += k[1,0]
        K[e+1,e+1] += k[1,1]

    K[e+1,e+1] += k[1,1]

    return K

def vec_force(X):
    '''constructing force vector '''

    F = np.zeros((X.size,1))
    x = 0
    for e in range(X.size-1):
        # length of the element
        dx = X[e+1] - X[e] 

        # assamble element body forces
        f = (dx/6)*np.dot(np.array([[2,1],[1,2]]),np.array([[forces(x-dx)],[forces(x)]]))

        # assemble global stiffness matrix
        F[e,0] += f[0,0]
        F[e+1,0] += f[1,0]

    F[e+1,0] += f[0,0]

    return F

def sol_num(X):
    '''returns vector of numerical solution of the displacement'''

    # Construct stiffness matrix
    K = mat_stiff(X)

    # Construct the force vector
    F = vec_force(X)

    # find the displacement 
    return np.linalg.solve(K,F)    # this uses LAPACK routine _gesv


if __name__ == '__main__':
    
    nel = 8                           # number of elements
    L   = 1.0                         # length
    dx  = L/nel                         # space increment (uniform)
    X   = np.arange(0.0,L,dx)           # vector of position of free elements

    # find numerical solution
    d = sol_num(X).reshape(X.size)
    # find the exact solution
    D = dspl_exact(X)
    
    # print the results
    if DEBUG:
        print("\nDisplacement (numerical):\n",d)
        print("\nExact displacement (computed analytically):\n",D)
        print("\nDifference between exact and numerical:\n",D-d)
        print("\nNorm of the difference:",np.linalg.norm(D-d))

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
