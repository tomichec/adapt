import numpy as np

from cure import dcure, viscos, CtK, ramp_temp, press_loc

DEBUG = 0

L = 1                         # length of the material
Nx = 10                       # number of space steps
dx = L/Nx                     # space step
assert (Nx*dx == L)

# estimate the maximal diffusion for the stability condition
max_permeab = 7e-6
min_viscos = 0.6
maxD = max_permeab/min_viscos

T = 3600*2                      # duration of the simulation
# dt = 0.1*(dx**2/(2*maxD))      # time step -- from stability condition
dt = 60
Nt = int(T/dt)                 # numer of time steps

# allocate the arrays for results
u = np.zeros((Nt,Nx))
du = np.zeros(Nx)
cure = np.zeros(Nt)
t = np.zeros(Nt)

# physical variables
g = 0                      # gravitational acceleration  -- is ignored
bc0 = 0                    # boundary condition at point 0

cure[0] = 1e-3                  # initial value of cure
permeab = 3.56e-06

# time loop
for j in range(0,Nt-1):

    u[j,0] = du[0] = bc0                  # bottom boundary
    # top boundary condition
    u[j,Nx-1] = du[Nx-1] = press_loc(j*dt)

    # space loop
    for i in range(1,Nx-1):
        # finite difference for the space
        du[i] = (u[j,i-1] - 2*u[j,i] + u[j,i+1])/(dx**2) - g
    
    time = dt*j
    t[j+1] = time
    temp = CtK(ramp_temp(time))
    u[j+1] = u[j] + dt*du*(permeab/viscos(temp,cure[j]))
    cure[j+1] = cure[j] + dt*dcure(temp,cure[j])

##################################################
# print the results

X = np.arange(0, L, dx)

# headers
print('000',end="")
for x in X:
    print('\t%.3f'% x, end="")
print()

# data
for time,line in zip(t,u):
    print(time, end="")
    for entry in line:
        print("\t", entry, end="")
    print()
