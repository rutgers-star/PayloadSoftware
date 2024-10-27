#!/usr/bin/env python

"""
A module which uses MatPlotLib to generate plots of collected the data for 1-Dimensional tests
"""

import matplotlib.pyplot as plt

__author__="Mike Fogel"
__credits__=["Mike Fogel", "Simon Kowerski"]
__credits__=["Mike Fogel", "Simon Kowerski"]
__creation_date__="7/26/2023"

def plot_sloshy(t, theta, theta_d, u, umotor, max_accel, err, errdot, ecumul):  
    """
    Uses MatPlotLib to generate plots of collected the data

    Args:
        t (?): time
        theta (float): current position as measured by the IMU. The current, measured angle of the satellite
        theta_d (float): desired position of the satellite. The guidance. Example "Move the test bench to 90 degrees", so theta_d=90
        u (float): calculated motor angular acceleration based on the PID controller
        umotor (float): same as u however in previous versions of the code, I wanted to store the calculated value (u) and the actual value (umotor) I was going to send. The actual value I was from the PID controller and the actual value = calculated value (u = umotor) unless the calculate value exceeded the max safety value. Then umotor = max_accel. This entire section no longer needs both u and u motor.
        max_accel (float): max allowed safety acceleration. It's a safety constraint.
        err (float: PID proportional error 
    """
        # Graph Solution
#    print("Starting GRAPHS")    
    fig,ax = plt.subplots(3,2)
    font = {'size'   : 3}
    plt.rc('font', **font)
    
    ax[0,0].plot(t,theta)
    ax[0,0].axhline(y=theta_d, color = 'r', linestyle = '-')
    ax[0,0].set_xlabel('t (s)')
    ax[0,0].set_ylabel('Tank')
    ax[0,0].set_ylim([-90,180])
    ax[0,0].set_xlim([0,t[-1]])
    ax[0,0].legend([r"$\theta$", r"$\theta_d$"], loc = "upper right")
    
    
    ax[0,1].plot(t,u)
    ax[0,1].plot(t,umotor)
    ax[0,1].axhline(y=max_accel, color = 'r', linestyle = '-')
    ax[0,1].axhline(y=-max_accel, color = 'r', linestyle = '-')
    ax[0,1].set_xlabel('t (s)')
    ax[0,1].set_ylabel('Controller')
    ax[0,1].set_ylim([-15000,15000])
    ax[0,1].set_xlim([0,t[-1]])
    ax[0,1].legend([r"$u_{calc}$", r"$u_{comamnd}$"], loc = "upper right")
    
    ax[1,0].plot(t,err)
    ax[1,0].set_xlabel('t (s)')
    ax[1,0].set_ylabel('Error')
    ax[1,0].set_xlim([0,t[-1]])
    ax[1,0].legend([r"$e(t)$"], loc = "upper right")
    
    ax[1,1].plot(t,errdot)
    ax[1,1].set_xlabel('t (s)')
    ax[1,1].set_ylabel('Error_dot')
    ax[1,1].set_xlim([0,t[-1]])
    ax[1,1].legend([r"$e_{dot}(t)$"], loc = "upper right")
    
    ax[2,0].plot(t,ecumul)
    ax[2,0].set_xlabel('t (s)')
    ax[2,0].set_ylabel('Cumul Error')
    ax[2,0].set_xlim([0,t[-1]])
    ax[2,0].legend([r"$e_{cum}(t)$"], loc = "upper right")
    
    ax[2,1].plot(t,ecumul)
    ax[2,1].set_xlabel('t (s)')
    ax[2,1].set_ylabel('Cumul Error')
    ax[2,1].set_xlim([0,t[-1]])
    ax[2,1].legend([r"$e_{cum}(t)$"], loc = "upper right")
    
    fig.tight_layout(pad=5.0)