#!/usr/bin/env python

"""
A module to run a 1-Dimensional test bench of the S.T.A.R. SPICEsat

Atributes:
#TODO: SIMON update these numbers to match BCT Wheel
    MAX_ITER: Max number of allowed iterations to meet desired angle
    MAX_ACCEL: Max acceleration in RPM/s of the maxon motor. SAFETY stop. 
    MAX_VEL: Max RPM of the maxon motor. SAFETY stop. 3500 is allowable.
"""

import math
import time
import subprocess
from ctypes import *
import numpy as np 
import matplotlib.pyplot as plt

from imu_control import init_imu, imu_data
from control import PID_control
from plot_tools import plot_sloshy
from dce_control import set_wheel_torque, set_wheel_speed

from Logs.log import log
from Logs.errors import ERROR


__author__="Mike Fogel"
__credits__=["Mike Fogel, Simon Kowerski, Serene Siu"]
__creation_date__="7/2/2023"

#TODO: SIMON update these numbers to match BCT Wheel
MAX_ITER=100        # Max number of allowed iterations to meet desired angle 
MAX_ACCEL=10000     # Max acceleration in RPM/s of the maxon motor. SAFETY stop.
MAX_VEL=3000        # Max RPM of the maxon motor. SAFETY stop. 3500 is allowable.

#TODO: SIMON have it end the running program
def end_experiment(error=False):
    """
    Ends the current experiment and make sure everything thing is return to its initial state

    Args:
    error (bool): True if error occured, False (default) if not

    """
    log(1402, "- output file: sloshing.h264")
    camlog.close()
    log(1403)

    set_wheel_speed(1,0)

    print("Plotting")    
    plot_sloshy(t, theta, theta_d, u, umotor, MAX_ACCEL, err, errdot, ecumul)
    plt.show()

    if error:
        log(2)
        
    else:
        log(1)

    exit(not error)

########### INITIAL VALUE CALCULATIONS START ###########
log(0)
# FIXME: Will need to redo for BCT Wheel?
# Reaction wheel Moment of Inertia
Jx=2.491E-4 # kg m^2
Jy=2.250E-4 # kg m^2
Jz=4.703E-4 # kg m^2
J=math.sqrt(Jx**2 + Jy**2 + Jz**2)
I=0.02344 # Full

# Initialization
theta_d=90 # Desired angle
tol=0.5    # Tolerance to angle reaching desired angle

# Proportional, Derivative, and Integral gains used in the PID controller algorithm
# Very close there as of 12/28/23
kp0=0.0075 
kd0=0.0015
ki0=0.001

# Freqency Response
wn=math.sqrt(kp0/I)
eta=kd0/(2*I*wn)
p=[1, 2*eta*wn, wn**2]
r=np.roots(p)

# Array Declarations of size MAX_ITER
k=1
t=np.empty(MAX_ITER)
theta=np.empty(MAX_ITER)
vel=np.empty(MAX_ITER)
acc=np.empty(MAX_ITER)
Omega=np.empty(MAX_ITER)
err=np.empty(MAX_ITER)
errdot=np.empty(MAX_ITER)
ecumul=np.empty(MAX_ITER)
u=np.empty(MAX_ITER)
umotor=np.empty(MAX_ITER)

# Initial conditions on key variables
meantheta=0
t[0]=0
err[0]=0
err[1]=0
errdot[0]=0
errdot[1]=0
ecumul[0]=0
ecumul[1]=0
tstart=time.time()
########### INITIAL VALUE CALCULATIONS END ###########

########### PRESSURE SENSOR STARTUP CODE BEGIN ##############

#EMPTY FOR NOW

########### PRESSURE SENSOR STARTUP CODE END ##############

########### MOTOR STARTUP CODE BEGIN ###########

#TODO: SIMON Run dce_control.is_active() to read from HR Run count, it throws an error if it doesn't work

########### MOTOR STARTUP CODE END ###########

########### IMU STARTUP CODE BEGIN ###########
try:
    yaw0,imu=init_imu()
    yawOld=0
    #print('Yaw0:',yaw0)
except Exception:
    end_experiment(True)
########### IMU STARTUP CODE END ###########

########### CAMERA STARTUP CODE BEGIN ###########
log(400)

#TODO: camera control module for proper error stuff
try:
    camlog=open("camlog.txt",'w')
    cam=subprocess.Popen(["/usr/local/bin/libcamera-vid", "-t 20000", "--nopreview", "--width", "960", "--height","540","--vflip","--saturation","0","--save-pts","camtimes.txt","--exposure","long","--framerate","24","-o","sloshing.h264"], text=True, stderr=camlog)

except Exception:
    end_experiment()

log(401)
########### CAMERA STARTUP CODE END ###########

########### MAIN CONTROL LOOP START ###########
while (k < MAX_ITER):
    t[k]=time.time() - tstart
    dt=t[k] - t[k-1]
    
# Get IMU data
    yaw,pitch,roll=imu_data(imu,yaw0,yawOld)
    theta[k]=yaw
    vel[k] = (theta[k]) - theta[k-1]/dt
    acc[k]=(vel[k] - vel[k-1])/dt
    err[k]=(theta[k] - theta_d)
    errdot[k]=(err[k] - err[k-1])/dt
    ecumul[k]=ecumul[k-1] + err[k]*dt

    # Control Algorithm Using PID Controller
    u[k] = PID_control(theta_d, k, t, dt, I, J, theta, vel, acc, err, errdot, ecumul)

    umotor[k]=u[k];
    acceleration=abs(umotor[k])
    if acceleration > MAX_ACCEL:
        acceleration=MAX_ACCEL

    velocity=np.sign(u[k])*MAX_VEL

    #Drive the Motor
    try:
        set_wheel_torque(1, u[k])
    except Exception:
        end_experiment()
    #TODO: Update this for new motor
    time.sleep(0.025) # Good as of 11/5/2023 10:51 am

    if (k > 10): 
        meantheta=np.mean(theta[k-10:k])

    yawOld=theta[k]
    k=k+1

########### MAIN CONTROL LOOP END ###########

end_experiment()