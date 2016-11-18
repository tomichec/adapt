import matplotlib.pyplot as plt
from math import exp

def CtK(C):return C+273.15
def KtC(C):return C-273.15

def dcure(T,cure):
    """Calculates the rate of cure given temperature 'T' and the degree of 'cure' """
    R = 8.617
    Aa = 1.53e5
    Ea = 6.65e4
    m = 0.813
    n = 2.74

    return Aa * exp(-Ea/(R*T)) * cure**m *(1-cure)**n

def viscos(T,alpha):
    """returns viscosity from the temperature 'T' and cure 'alpha' """
    # viscosity
    R = 8.617
    muinf = 3.45e-10		# steady-state viscosity (GPa s)
    E_mu = 7.6536e4             # activation energy (J/mol)
    alpha_g = 0.47              # degree of cure at gelation
    A = 3.8
    B = 2.5

    if ( alpha < (0.46) ) :
        return muinf *exp(E_mu/(R*T)) * ( alpha_g/(alpha_g-alpha))**(A+B*alpha)
    else:
        return 1e8


def ramp_temp(time):
    """ gives temperature in centigrades as a function of 'time' from the experimental temperature protocol"""
    # temperatures
    Tinit = 30
    Tflow = 107.222
    Tcure = 176.66667

    # time in minutes
    duration_ramp1 = 30*60
    duration_flow  = 30*60
    duration_ramp2 = 30*60
    duration_cure  = 60*60

    time1 = duration_ramp1
    time2 = time1 + duration_flow
    time3 = time2 + duration_ramp2
    time4 = time3 + duration_cure
    
    if (time >= 0 and time < time1):
        return (Tflow-Tinit)/duration_ramp1 * time + Tinit
    elif (time >= time1 and time < time2):
        return Tflow
    elif (time >= time2 and time < time3):
        return (Tcure-Tflow)/duration_ramp2 * (time-time2) + Tflow
    elif (time >= time3 and time < time4):
        return Tcure
    else:
        return Tcure

def press_loc(time):
    """ gives the possition of the press as a function of 'time' --  press protocol"""

    # temperatures
    Binit = -0
    Bflow = -0.001

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


    
if __name__ == '__main__':

    dt = 60                        # time step (1/s)
    dur = 2*3600                      # duration of the simulation (s)
    N = int(dur/dt)                   # number of time steps

    # initial condition
    time = 0
    cure = 0.001                   
    temp = 30

    print(time,temp,cure)

    # time-stepping algorithm (forward Euler)
    for i in range(N):
        temp = CtK(ramp_temp(time))
        cure += dt*dcure(temp,cure)
        time += dt

        # output results
        print(time,KtC(temp),cure)
