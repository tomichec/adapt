#!/usr/bin/python3

import numpy as np
import sys
import argparse

##################################################
# treat warnings as exceptions
# http://stackoverflow.com/questions/15933741/how-do-i-catch-a-numpy-warning-like-its-an-exception-not-just-for-testing
import warnings

warnings.filterwarnings('error')

# the warnings are treated as exceptions. This is because the
# simulation is unstable for specific combination of dt and dx. Then
# the results get erroreous values which make the simulation release
# warnings. However, since the results do not make sense at this
# point, it can be just treated as error.

##################################################
# import for the model 
from cure import viscos, vfrac, perm, stress, CtK

def print_results(t, u,tfmt='%.08f',every = 1):
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
    L = 1e-2                         # length of the material (m)
    Nx = args.nodes                       # number of space steps
    dx = L/Nx                     # space step
    assert (Nx*dx == L)

    if args.optimal_dt:
        dt = round(0.8*(dx**2/2),3) # time step -- from stability condition
        print("Optimal  step size is dt=", dt,file=sys.stderr)
    else:
        dt = args.time_step  # time step -- from the command line argument


    T = 30                     # duration of the simulation
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
    ppt = 1.0                  # printing period of time
    pft = int(round(ppt/dt,6)) # printing frecuency of time (TODO: check what happens when dt=1e-{5,9,15}, the round is a quick way around)
    assert (pft*dt == ppt)      # assert if the printing period is compatible with the time step size

    ppx = L*0.1                   # printing period of space
    pfx = int(ppx/dx)           # printing frecuency of space (every column)
    assert (pfx*dx == ppx)      # assert if the printing period is compatible with the time step size

    # print headers
    print('000',end="")         # dummy time header
    for i in range(0,Nx+1,pfx):
        print('\t%.3f'% (i*dx), end="") # print frame of reference
    print()

    print_results(0,u,every = pfx)          # print initial conditioins

    # initial conditions
    cure = 0
    T = CtK(150)
    Patm = 0.1                 # atmospheric pressure (MPa)
    young = 1.                # Young modulus (for carbon fibre ~50 (MPa))

    # j is index for time, and i is index for space, the order of time and
    # space is swaped wrt report.pdf
    for j in range(1,Nt):

        # finite difference for the space
        strain_prev = (u[1] - 0)/dx # imposes bottom boundary condition (u[0] = 0)
        efstr_prev = stress(vfrac(strain_prev))
        for i in range(1,Nx):
            # strain for permeability at current point
            strain = (u[i+1] - u[i-1])/(2*dx)

            # Vf at next point
            strain_next = (u[i+1] - u[i])/dx
            efstr_next = stress(vfrac(strain_next))

            # finite difference
            du[i] = -(perm(vfrac(strain))/viscos(T,cure))*(efstr_next - efstr_prev)/dx

            # update the volume fraction for the next point
            efstr_prev = efstr_next

        # bottom boundary is implicitely imposed as du[0] = 0

        # impose top boundary condition
        strain = strain_next        # for permeability at current point
        efstr = efstr_next
        du[Nx] = -(perm(vfrac(strain))/viscos(T,cure))*(Patm - efstr)/dx

        # update the increment
        u += dt*du*young

        # cure dynamics -- decoupled from the space calculation
        # temp = CtK(ramp_temp(time))
        # cure = cure + dt*dcure(temp,cure)

        # print the results
        if not (j % pft):
            print_results(dt*j,u,every = pfx)
