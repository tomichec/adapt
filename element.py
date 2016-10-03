import numpy as np

# def LM(a,e):
#     if a == 0:
#         return e
#     if a == 1:
#         return e+1

if __name__ == '__main__':

    nel = 8
    L = 1.0
    h = L/nel
    
    # assamble local stiffness matrix (this was computed by hand)
    k = (1/h)*np.matrix([[1,-1],[-1,1]])
    
    # assemble global stiffness matrix
    K = np.zeros((nel+1,nel+1))
    for e in range(nel-1):
        K[e,e] += k[0,0]
        K[e,e+1] += k[0,1]
        K[e+1,e] += k[1,0]
        K[e+1,e+1] += k[1,1]
    
    print("global stiffness matrix:\n",K)
    
