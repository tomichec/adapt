# Hughs p 36 Excercise 1

# DEBUG flag: 1 to print extra information, 0 to avoid printing
DEBUG = 1

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt

def dshape_x(A,x,h):
    '''defines the derivative (with respect to x) of piecewise linear shape function for A'''
    c = A*h                     # center of the shape function

    # DIRTY HACK -- CORRECT
    if x < 0 or x > 1:
        return 0

    if c-h <= x and x <= c:
        return 1./h
    elif c < x and x <= c+h:
        return -1./h
    else:
        return 0

def shape(A,x,h):
    '''defines the piecewise linear shape function for A'''
    c = A*h                     # center of the shape function
    if x < 0 or x > 1:
        return 0
    if c-h <= x and x <= c:
        return (x- (c-h))/h
    elif c < x and x <= c+h:
        return ((c+h) - x)/h
    else:
        return 0


if __name__ == '__main__':
    
    nel = 10                           # number of elements
    L = 1.0                         # length
    h = L/nel                         # space increment (uniform)
    X = np.linspace(0,L,nel+1)        # linear space
    q = -1.                         # constant of the body forces
    
    # Construct stiffness matrix
    K = np.zeros((nel+1,nel+1))
    for i in range(nel):
        for j in range(nel+1):
            I = integrate.quad(lambda x:(dshape_x(i,x,h)*dshape_x(j,x,h)),(i-2)*h,(i+2)*h)
            K[i,j] = I[0]
            # print integration error
            # if abs(i - j) < 2:
            #     print(i,j,I[1])
    
    K[nel,nel] = 1                      # stiffness on the boundary
    
    # Construct the force vector
    F = np.matrix(np.zeros((nel+1,1)))
    for i in range(nel):
        I = integrate.quad(lambda x:(shape(i,x,h)*q),(i-2)*h,(i+2)*h) # returns tupple (integral, error)
        F[i,0] = I[0]
        
    # find the displacement using the matrix inverse
    d = np.linalg.inv(K)*F
    
    # compare results with the exact solution
    u = [] 
    norm = 0
    for x,dis in zip(X,d):
        exact = q/2 *(1-x**2)   # NEEDS TO CHANGE
        u.append([exact])           # analytical solution
        norm += (dis-exact)**2
    
    U = np.matrix(u)
    dfr = U-d              # difference between exact and numerical
    norm = np.sqrt(norm)
    
    # print the results
    if DEBUG:
        print("Stiffness matrix K:\n",K)
        print("\nForce vector F:\n",F)
        print("\nDisplacement (numerical):\n",d)
        print("\nExact displacement (computed analytically):\n",U)
        print("\nDifference between exact and numerical:\n",dfr)
        print("\nNorm of the difference:",norm)
    
    
    # plot the results
    f=plt.figure(1)
    plt.plot(X,d,'ro-')
    plt.ylabel("displacement")
    plt.xlabel("x")
    # plt.savefig('displacement.eps', format='eps', dpi=1000)
    plt.show()
