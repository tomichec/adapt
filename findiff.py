import numpy as np

DEBUG = 0

L = 1                         # length of the material
Nx = 10                       # number of space steps
dx = L/Nx                     # space step
assert (Nx*dx == L)

T = 0.404                      # duration of the simulation
dt = 0.8*(dx**2/2)             # time step -- from stability condition
Nt = int(T/dt)                 # numer of time steps


# physical variables
g = 0                      # gravitational acceleration  -- is ignored
R = -0.1                   # speed of the press shift
NR = int(0.2/dt)           # number of steps the press shifts
bc0 = 0                    # boundary condition at point 0


# allocate the arrays for results
u = np.zeros((Nt,Nx))
t = np.zeros(Nt)
X = np.arange(0, L, dx)
du = np.zeros(Nx)

for j in range(0,Nt-1):

    u[j,0] = du[0] = bc0                  # bottom boundary
    # top boundary condition
    # u[j,Nx-1] = du[Nx-1] = R*dt*(j+1)
    if j < NR:
        u[j,Nx-1] = du[Nx-1] = R*dt*(j)
    else:
        u[j,Nx-1] = du[Nx-1] = R*dt*NR

    for i in range(1,Nx-1):
        # finite difference for the space
        du[i] = (u[j,i-1] - 2*u[j,i] + u[j,i+1])/(dx**2) - g

    t[j+1] = dt*j
    u[j+1] = u[j] + dt*du

##################################################
# print the results

# headers
print("time",end="")
for x in X:
    print("\t", x, end="")
print()

# data
for time,line in zip(t,u):
    print(time, end="")
    for entry in line:
        print("\t", entry, end="")
    print()
