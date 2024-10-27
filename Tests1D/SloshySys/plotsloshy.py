# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 16:41:09 2023

@author: mfogel
"""

import matplotlib.pyplot as plt

def plotsloshy(t, theta, theta_d, u, umotor, umax, Omega, vel, acc, err, errdot, ecumul):

    
    # Graph Solution
#    print("Starting GRAPHS")    
#    fig,ax = plt.subplots(3,2)
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
#    ax[0,1].plot(t,Omega)
    ax[0,1].axhline(y=umax, color = 'r', linestyle = '-')
    ax[0,1].axhline(y=-umax, color = 'r', linestyle = '-')
    ax[0,1].set_xlabel('t (s)')
    ax[0,1].set_ylabel('Controller')
    ax[0,1].set_ylim([-15000,15000])
    ax[0,1].set_xlim([0,t[-1]])
#    ax[0,1].legend([r"$u_{calc}$", r"$u_{comamnd}$", r"$\Omega$"], loc = "upper right")
    ax[0,1].legend([r"$u_{calc}$", r"$u_{comamnd}$"], loc = "upper right")
    
    
#    ax[1,0].plot(t,vel)
#    ax[1,0].set_xlabel('t (s)')
#    ax[1,0].set_ylabel('Tank Vel')
#    ax[1,0].set_xlim([0,t[-1]])
#    ax[1,0].set_ylim([-1000,1000])
#    ax[1,0].legend([r"$\omega$"], loc = "upper right")
    
#    ax[1,1].plot(t,acc)
#    ax[1,1].set_xlabel('t (s)')
#    ax[1,1].set_ylabel('Tank Acc')
#    ax[1,1].set_xlim([0,t[-1]])
#    ax[1,1].set_ylim([-1000,1000])
#    ax[1,1].legend([r"$\omega_{dot}$"], loc = "upper right")
    
    ax[2,0].plot(t,err)
    ax[2,0].set_xlabel('t (s)')
    ax[2,0].set_ylabel('Error')
    ax[2,0].set_xlim([0,t[-1]])
    ax[2,0].legend([r"$e(t)$"], loc = "upper right")
    
    ax[2,1].plot(t,errdot)
    ax[2,1].set_xlabel('t (s)')
    ax[2,1].set_ylabel('Error_dot')
    ax[2,1].set_xlim([0,t[-1]])
    ax[2,1].legend([r"$e_{dot}(t)$"], loc = "upper right")
    
    ax[3,0].plot(t,ecumul)
    ax[3,0].set_xlabel('t (s)')
    ax[3,0].set_ylabel('Cumul Error')
    ax[3,0].set_xlim([0,t[-1]])
    ax[3,0].legend([r"$e_{cum}(t)$"], loc = "upper right")
    
    ax[3,1].plot(t,ecumul)
    ax[3,1].set_xlabel('t (s)')
    ax[3,1].set_ylabel('Cumul Error')
    ax[3,1].set_xlim([0,t[-1]])
    ax[3,1].legend([r"$e_{cum}(t)$"], loc = "upper right")
    
    fig.tight_layout(pad=5.0)
    
    #print("END GRAPHS")  