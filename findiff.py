import numpy as np
import sys
import argparse

DEBUG = 0

def print_results(t, u,tfmt='%.02f',every = 1):
    """Print results of the heat equation at time 't' in time format 'tfmt' and every 'every' column of deformation 'u'."""
    print(tfmt % t, end="")
    for i in range(0,len(u),every):
        print("\t%.15g" % (u[i]), end="")
    print()

if __name__ == '__main__':

    #######################################################
    # get options from command line

    # initialize the parser
    parser = argparse.ArgumentParser(#usage="%(prog)s [options]",
                                     description="Finite difference solver.")

    # time step
    parser.add_argument("-t","--time-step",
                        type=float, 
                        default=0.004,
                        help="integration time step (default 0.004)")

    # space step
    parser.add_argument("-n","--nodes",
                        type=int, 
                        default=10,
                        help="number of nodes in space (default 10)")

    # select an optimal time step size
    # TODO: make it mutualy exclusive with --time-step option
    parser.add_argument("-o",
                        "--optimal-dt",
                        action="store_true",
                        help="overwrites the time step size with an optimal value.")

    # parse arguments into args variable.
    args = parser.parse_args()

    ##################################################
    # setup the solver
    L = 1                         # length of the material
    Nx = args.nodes                       # number of space steps
    dx = L/Nx                     # space step
    assert (Nx*dx == L)

    if args.optimal_dt:
        dt = round(0.8*(dx**2/2),3) # time step -- from stability condition
        print("Optimal  step size is dt=", dt,file=sys.stderr)
    else:
        dt = args.time_step  # time step -- from the command line argument


    T = 0.5                     # duration of the simulation
    Nt = int(T/dt)+1            # numer of time steps

    # allocate the arrays for results
    u = np.zeros(Nx+1)            # initial conditions
    du = np.zeros(Nx+1)           # allocate array for solution increments

    ##################################################
    # setup the model
    g = 0                      # gravitational acceleration  -- is ignored
    R = -0.1                   # speed of the press shift
    NR = int(0.2/dt)           # number of steps the press shifts
    bc0 = 0                    # boundary condition at point 0

    ##################################################
    # setup the printing
    ppt = 0.02                  # printing period of time
    pft = int(ppt/dt)           # printing frecuency of time (TODO: check what happens when dt=1e-5, the round is a quick way around)
    assert (pft*dt == ppt)      # assert if the printing period is compatible with the time step size

    ppx = 0.1                   # printing period of space
    pfx = int(ppx/dx)           # printing frecuency of space (every column)
    assert (pfx*dx == ppx)      # assert if the printing period is compatible with the time step size

    # print headers
    print('000',end="")         # dummy time header
    for i in range(0,Nx+1,pfx):
        print('\t%.1f'% (i*dx), end="") # print frame of reference
    print()

    print_results(0,u,every = pfx)          # print initial conditioins

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

        u = u + dt*du

        # print the results
        if not (j % pft):
            print_results(dt*j,u,every = pfx)
