import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm

from cure import dcure, viscos, CtK, ramp_temp

DEBUG = 0

def press_loc(time):
    """ gives the possition of the press as a function of 'time' --  press protocol"""

    # temperatures
    Binit = -0
    Bflow = -0.0001

    time1 = 30*60
    time2 = 60*60
    time3 = 120*60
    
    if (time >= 0 and time < time1):
        return 0
    elif (time >= time1 and time < time2):
        return (Bflow-Binit)/(time2-time1) * (time-time1) + Binit
    elif (time >= time2 and time < time3):
        return Bflow
    else:
        return Bflow


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
    temp = CtK(ramp_temp(time))
    u[j+1] = u[j] + dt*du*(permeab/viscos(temp,cure[j]))
    cure[j+1] = cure[j] + dt*dcure(temp,cure[j])




mpl.rcParams.update({'font.size': 16})

f=plt.figure(1,figsize=(6,4))
plt.margins(0.05, 0.1)

t = np.arange(0, T, dt)
x = np.arange(0, L, dx)


plt.plot(x,u[0],'bv-',label = "initial")
plt.plot(x,u[int(Nt/4)],'m^-',label = "$t=%.3f$ min" % (Nt/4*dt/60)) 
plt.plot(x,u[int(Nt/2)],'g+-',label = "$t=%.3f$ min" % (Nt/2*dt/60))
plt.plot(x,u[Nt-1],'ro-',label = "$t=%.3f$ min" % (Nt*dt/60))
plt.ylabel("displacement $u$")
plt.xlabel("reference frame $X$")
plt.legend(loc='lower left')
if DEBUG:
    plt.show()
else:
    plt.savefig('flow_phys.eps', format='eps', dpi=1000,bbox_inches='tight')

f=plt.figure(2,figsize=(6,4))
plt.margins(0.05, 0.1)

t = np.arange(0, T, dt)/60

# plot deformation with respect to time
plt.plot(t,u[:,0],'b-',label = "$x=0$")
plt.plot(t,u[:,int(Nx/4)],'m-',label = "$x=%.3g$" % (int(Nx/4)*dx)) 
plt.plot(t,u[:,int(Nx/2)],'g-',label = "$x=%.3g$" % (int(Nx/2)*dx))
plt.plot(t,u[:,Nx-1],'r-',label = "$x=%.3g$" % (Nx*dx))
plt.ylabel("displacement $u$")
plt.xlabel("time $t$")
plt.legend(loc='lower left',frameon=False)
if DEBUG:
    plt.show()
else:
    plt.savefig('deform_phys.eps', format='eps', dpi=1000,bbox_inches='tight')


# 3d plot
fig = plt.figure(3,figsize=(6,4))

plt.imshow(u,aspect='auto')
plt.colorbar()                  # shrink=0.8, aspect=20


xticks = plt.xticks()
yticks = plt.yticks()

plt.xticks(xticks[0],xticks[0]*dx)
plt.yticks(yticks[0],yticks[0]*dt)

plt.xlim([0, Nx])
plt.ylim([Nt, 0])

plt.xlabel("reference frame $X$")
plt.ylabel("time $t$")

if DEBUG:
    plt.show()
else:
    plt.savefig('surf_phys.eps', format='eps', dpi=30,bbox_inches='tight')


fig = plt.figure(4,figsize=(6,4))
for i in range(Nt):
    plt.plot(x,u[i],'m^-',label = "$t_{%d}=%.0f$ min" % (i, i*dt/60)) 
    plt.legend(loc='lower left',frameon=False)
    plt.xlabel("reference frame $X$")
    plt.ylabel("displacement $u$")
    plt.ylim([-0.007,0.0001])
    plt.savefig("test/movie%03d.png" % i)
    plt.cla()



# ax = fig.gca(projection='3d')
# ax.view_init(elev=90., azim=0)

# X, Y = np.meshgrid(X, Y)

# surf = ax.plot_surface(X, Y, u, rstride=1, cstride=1, cmap=cm.jet,linewidth=0)
# for ii in range(360):
#     ax.view_init(elev=10., azim=ii)
#     plt.savefig("test/movie%d.png" % ii)

