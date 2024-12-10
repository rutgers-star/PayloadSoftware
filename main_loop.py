#!/usr/bin/env python

"""
A module to run a 1-Dimensional test bench of the S.T.A.R. SPICEsat

Atributes:
    MAX_ITER: Max number of allowed iterations to meet desired angle
    #QUESTION: DO we need max accel anymore - maybe max velocity instead
    MAX_ACCEL: Max acceleration in RPM/s of the maxon motor. SAFETY stop. 
    MAX_VEL: Max RPM of the reaction wheel. 6553.4 rpm is the largest allowed
"""

import math
import time
import subprocess
from ctypes import *
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

from imu_control import init_imu, imu_data
from camera_control import init_camera, close_camera
from control import PID_control
from plot_tools import plot_sloshy
from dce_control import set_wheel_torque, set_wheel_speed, dce_startup

from Logs.log import log
from Logs.errors import ERROR


__author__="Mike Fogel"
__credits__=["Mike Fogel", "Simon Kowerski", "Serene Siu"]
__credits__=["Mike Fogel", "Simon Kowerski", "Serene Siu"]
__creation_date__="7/2/2023"

MAX_ITER=100        # Max number of allowed iterations to meet desired angle 
MAX_ACCEL=10000     # Max acceleration in RPM/s of the maxon motor. SAFETY stop.
MAX_VEL=6553.4        # Max RPM of the reaction wheel. 6553.4 rpm is the largest allowed

def hardware_startup():
    """
    Opens all connections to necessary hardware
    """
    ########### PRESSURE SENSOR STARTUP CODE BEGIN ##############

    #EMPTY FOR NOW

    ########### PRESSURE SENSOR STARTUP CODE END ##############

    ########### DCE/RW STARTUP CODE BEGIN ###########

    try:
        dce_startup()
    except ERROR:
        log(2)
        exit()

    ########### DCE/RW STARTUP CODE END ###########

    ########### IMU STARTUP CODE BEGIN ###########
    
    try:
        global yaw0, imu, yawOld
        yaw0,imu=init_imu()
        yawOld=0
    except ERROR:
        end_experiment(True)

    ########### IMU STARTUP CODE END ###########

    ########### CAMERA STARTUP CODE BEGIN ###########
    
    try:
        init_camera()
    except ERROR:
        end_experiment(True)
    
    ########### CAMERA STARTUP CODE END ###########

def end_experiment(error=False):
    """
    Ends the current experiment and make sure everything thing is return to its initial state

    Args:
        error (bool): true if error occured, false (default) if not
    """
    close_camera()

    try:
        set_wheel_speed(1,0)
    except ERROR:
        pass

    #TODO: Figure this out later
    plot_sloshy(t, theta, theta_d, u, umotor, MAX_ACCEL, err, errdot, ecumul)
    plt.show()

    if error:
        log(2)
        
    else:
        log(1)

    exit()

#TODO: Documentation
def experiment_reader(experiment_name):
    """
    
    Returns:
        LocIndexerFrame: an "array" which contains fields accessed by name (ex. arr["Experiment #"])
        \n\tValues include: 
        -Experiment #
        -Phase
        -Angle
        -Velocity
        -Mission Day
        -Maneuver
        -Rotation Axis
        -Camera
        -Controller
    """
    filename='Experiment Design.xlsx'
    sheet='Experiment Design V2'
    cols=[1,2,3,4,5,6,7,8,9,12]

    dataframe = pd.read_excel(filename, sheet_name=sheet, usecols=cols, header=1, nrows=234, index_col=2)
    return dataframe.loc[experiment_name]

########### INITIAL VALUE CALCULATIONS START ###########
log(0)
# Reaction wheel Moment of Inertia
"""
Jx=2.491E-4 # kg m^2
Jy=2.250E-4 # kg m^2
Jz=4.703E-4 # kg m^2
"""

Jx=6.41E-5 # kg m^2
Jy=6.46E-5 # kg m^2
Jz=1.151E-4 # kg m^2

J=math.sqrt(Jx**2 + Jy**2 + Jz**2)
# QUESTION: What this vvv
I=0.02344 # Full

# Initialization
theta_d=90 # Desired angle
tol=0.5    # Tolerance to angle reaching desired angle

# TODO: MIKE update for new wheel
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

hardware_startup()

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
    velocity=np.sign(u[k])*MAX_VEL

    #Drive the Motor
    try:
        set_wheel_torque(1, u[k])
    except ERROR:
        end_experiment(True)
        
    #TODO: MIKE Update this for new motor
    time.sleep(0.025) # Good as of 11/5/2023 10:51 am

    if (k > 10): 
        meantheta=np.mean(theta[k-10:k])

    yawOld=theta[k]
    k=k+1

########### MAIN CONTROL LOOP END ###########

end_experiment()