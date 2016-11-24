import numpy as np

DEBUG = 0

if __name__ == '__main__':
    L = 1                         # length of the material
    Nx = 10                       # number of space steps
    dx = L/Nx                     # space step
    assert (Nx*dx == L)

    T = 0.5                      # duration of the simulation
    dt = round(0.8*(dx**2/2),3)             # time step -- from stability condition
    Nt = int(T/dt)+1                 # numer of time steps


    # physical variables
    g = 0                      # gravitational acceleration  -- is ignored
    R = -0.1                   # speed of the press shift
    NR = int(0.2/dt)           # number of steps the press shifts
    bc0 = 0                    # boundary condition at point 0

    # allocate the arrays for results
    u = np.zeros(Nx+1)            # initial conditions
    du = np.zeros(Nx+1)           # allocate array for solution increments

    # print frame of reference in headers
    print('000',end="")
    for i in range(Nx+1):
        print('\t%.3f'% (i*dx), end="")
    print()

    # print initial conditions
    print('%.03f' % 0, end="")
    for entry in u:
        print("\t", entry, end="")
    print()

    # j is index for time, and i is index for space, the order of time and
    # space is swaped wrt report.pdf
    for j in range(1,Nt):

        # boundary conditions...
        u[0] = bc0                  # ...at the bottom,...
        # ... and at the top
        if j < NR:
            u[Nx] = R*dt*(j)
        else:
            u[Nx] = R*dt*NR

        # # numerical boundary conditions
        # du[0] = 2*(u[1] -2*u[0])/dx**2
        # du[Nx-1] = 0

        # finite difference for the space
        for i in range(1,Nx):
            du[i] = (u[i-1] - 2*u[i] + u[i+1])/(dx**2) - g

        t = dt*j
        u = u + dt*du

        # print the results
        print('%.03f' % t, end="")
        for entry in u:
            print("\t", entry, end="")
        print()

