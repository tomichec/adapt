# Hughs p 36 Excercise 1

# DEBUG flag: 1 to print extra information, 0 to avoid printing
DEBUG = 1

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt

# benchmarking
import time

def dshape_x(A,x,dx):
    '''defines the derivative (with respect to x) of piecewise linear shape function for A'''
    c = A*dx                     # center of the shape function

    # Hardcoded limits for shape functions TODO: CORRECT
    if x < 0 or x > 1:
        return 0

    if c-dx <= x and x <= c:
        return 1./dx
    elif c < x and x <= c+dx:
        return -1./dx
    else:
        return 0

def shape(A,x,dx):
    '''defines the piecewise linear shape function for A'''
    c = A*dx                     # center of the shape function

    # Hardcoded limits for shape functions TODO: CORRECT
    if x < 0 or x > 1:
        return 0

    if c-dx <= x and x <= c:
        return (x- (c-dx))/dx
    elif c < x and x <= c+dx:
        return ((c+dx) - x)/dx
    else:
        return 0

def dspl_exact(x):
    '''exact displacement for our problem'''
    return q/2 *(1-x**2)



if __name__ == '__main__':
    
    nel = 8                           # number of elements
    L   = 1.0                         # length
    dx  = L/nel                         # space increment (uniform)
    X   = np.arange(0.0,L,dx)           # vector of position of free elements
    q   = -1.                         # constant of the body forces
    
    # Construct stiffness matrix
    print('Constructing stiffness matrix:',end='\t')
    start = time.time()
    K = np.zeros((nel,nel))
    for i in range(nel):
        for j in range(nel):
            #  for linear system we have only one neighbouring point
            #  at each side, hence the integration simplifies as
            if abs(i-j) <2:
                I = integrate.quad(lambda x:(dshape_x(i,x,dx)*dshape_x(j,x,dx)),(i-1)*dx,(i+1)*dx)
                K[i,j] = I[0]

    print(time.time()-start)

    # Construct the force vector
    print('Constructing force vector:',end='\t')
    start = time.time()
    F = np.matrix(np.zeros((nel,1)))
    for i in range(nel):
        I = integrate.quad(lambda x:(shape(i,x,dx)*q),(i-1)*dx,(i+1)*dx) # returns tupple (integral, error)
        F[i,0] = I[0]

    print(time.time()-start)        

    # find the displacement 
    print('Solving the system:',end='\t')
    start = time.time()
    # d = np.linalg.inv(K)*F    # this invert the stiffness matrix 
    d = np.linalg.solve(K,F)    # this uses LAPACK routine _gesv
    print(time.time()-start)        
    
    # compare results with the exact solution
    u = [] 
    norm = 0
    for x,dis in zip(X,d):
        u.append([dspl_exact(x)])
        norm += (dis-dspl_exact(x))**2
    
    U = np.matrix(u)
    dfr = U-d              # difference between exact and numerical
    norm = np.sqrt(norm)
    
    # print the results
    if DEBUG:
        print("\nStiffness matrix K:\n",K)
        print("\nForce vector F:\n",F)
        print("\nDisplacement (numerical):\n",d)
        print("\nExact displacement (computed analytically):\n",U)
        print("\nDifference between exact and numerical:\n",dfr)
        print("\nNorm of the difference:",norm)
    

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
        plt.savefig('displacement.eps', format='eps', dpi=1000)
