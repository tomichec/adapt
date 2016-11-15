mpl.rcParams.update({'font.size': 16})

f=plt.figure(1,figsize=(6,4))
plt.margins(0.05, 0.1)

x = np.arange(0, L, dx)

# plot deformation with respect to reference frame
plt.plot(x,u[0],'bv-',label = "initial")
plt.plot(x,u[int(Nt/4)],'m^-',label = "$t=%.3g$" % (int(Nt/4)*dt)) 
plt.plot(x,u[int(Nt/2)],'g+-',label = "$t=%.3g$" % (int(Nt/2)*dt))
plt.plot(x,u[Nt-1],'ro-',label = "$t=%.3g$" % (Nt*dt))
plt.ylabel("displacement $u$")
plt.xlabel("reference frame $X$")
plt.legend(loc='lower left',frameon=False)
if DEBUG:
    plt.show()
else:
    plt.savefig('flow.eps', format='eps', dpi=1000,bbox_inches='tight')


f=plt.figure(2,figsize=(6,4))
plt.margins(0.05, 0.1)

t = np.arange(0, T-dt, dt)

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
    plt.savefig('deform.eps', format='eps', dpi=1000,bbox_inches='tight')



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
    plt.savefig('surf.eps', format='eps', dpi=30,bbox_inches='tight')

# ax = fig.gca(projection='3d')
# ax.view_init(elev=90., azim=0)

# X, Y = np.meshgrid(X, Y)

# surf = ax.plot_surface(X, Y, u, rstride=1, cstride=1, cmap=cm.jet,linewidth=0)
# for ii in range(360):
#     ax.view_init(elev=10., azim=ii)
#     plt.savefig("test/movie%d.png" % ii)
