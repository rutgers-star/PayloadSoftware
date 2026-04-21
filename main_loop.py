#!/usr/bin/env python

"""
A module to run a 1-Dimensional test bench of the S.T.A.R. SPICEsat

Atributes:
    MAX_ITER: Max number of allowed iterations to meet desired angle
    #QUESTION: DO we need max accel anymore - maybe max velocity instead?
    MAX_ACCEL: Max acceleration in RPM/s of the maxon motor. SAFETY stop. 
    MAX_VEL: Max RPM of the reaction wheel. 6553.4 rpm is the largest allowed

    CAMERA: whether or not the CAMERA is being used in the current experiment
    SPINNING: used to keep track of whether or not the reaction wheel is SPINNING, not to be changed by the user
"""

from datetime import date
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
from plot_tools import plot_sloshy, plotforcestorques
from dce_control import set_wheel_torque, set_wheel_speed, dce_startup, read_data
from led_control import init_led, led_off, led_on, close_led
from sensor_control import sensor_start, sensor_read, sensor_stop
from ExperimentReader.get_experiment import get_experiment, Experiment

from Logs.log import log
from Logs.errors import ERROR


__author__="Mike Fogel"
__credits__=["Mike Fogel", "Simon Kowerski", "Serene Siu"]
__creation_date__="7/2/2023"

#TODO: Update these - we need a max torque to prevent the ADCS software throwing an error
MAX_ITER=600          # Max number of allowed iterations to meet desired angle 

CAMERA=False            # Whether or not camera being used during current experiment
SPINNING=False          # Whether or not the wheel is currently spinning. DO NOT CHANGE THIS VARIABLE.

__gExpLogPath="Logs/ExpLogs/"

def hardware_startup(experiment: Experiment):
    """
    Opens all connections to necessary hardware. If an error occurs, program exits and codes are logged
    """
    global CAMERA
    CAMERA = experiment.camera
    ########### PRESSURE SENSOR STARTUP CODE BEGIN ##############

    #EMPTY FOR NOW

    ########### PRESSURE SENSOR STARTUP CODE END ##############

    ########### DCE/RW STARTUP CODE BEGIN ###########

    try:
        dce_startup()
    except ERROR:
        end_experiment(True)

    global bota_ft_sensor_driver
    try:
        bota_ft_sensor_driver = sensor_start("bota_binary_gen0.json")
    except ERROR:
        end_experiment(True)

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
    #TODO: don't change constant find another way to validate in end_experiment
        
    if CAMERA:
        try:
            init_led(pin=17)        
            init_camera()
            led_on()
        except ERROR:
            end_experiment(True)
    else:
        log(3)
    
    ########### CAMERA STARTUP CODE END ###########

def end_experiment(error=False):
    global t, theta, theta_d, u, umotor, err, errdot, ecumul, force, torque
    """
    Ends the current experiment and make sure everything thing is return to its initial state

    Args:
        error (bool): true if error occured, false (default) if not
    """
    sensor_stop(bota_ft_sensor_driver)
    if(CAMERA):
        close_camera()
        led_off()
        close_led()

    if(SPINNING):
        try:
            set_wheel_speed(1,0)
        except ERROR:
            try:
                raise ERROR(1001)
            except ERROR:
                log(99)
                exit(1001)

        #TODO: Figure this out later
        plot_sloshy(t, theta, theta_d, u, umotor, err, errdot, ecumul)
        plotforcestorques(t, u, force, torque)
        plt.show()

    if error:
        log(2)
        
    else:
        log(1)
    exit()

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
# TODO: Recieve and update value from mike
#I=0.02344 # Full
I=0.05

# Initialization
theta_d=90 # Desired angle
tol=0.5    # Tolerance to angle reaching desired angle

# TODO: update for new wheel
# Proportional, Derivative, and Integral gains used in the PID controller algorithm
# Very close there as of 12/28/23
kp0=0.0075 
kd0=0.0015
ki0=0.001
kt0 = 0.01 # NEW: For torque sensor 

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
force = np.empty((MAX_ITER,3))
torque = np.empty((MAX_ITER,3))
yaw = np.zeros(MAX_ITER)
pitch = np.zeros(MAX_ITER)
roll = np.zeros(MAX_ITER)
dyawdt = np.zeros(MAX_ITER)
dpitchdt = np.zeros(MAX_ITER)
drolldt = np.zeros(MAX_ITER)
ddyawdt2 = np.zeros(MAX_ITER)
ddpitchdt2 = np.zeros(MAX_ITER)
ddrolldt2 = np.zeros(MAX_ITER)

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

def start_experiment(experiment_num: int):
    global k, yawOld

    experiment = get_experiment(experiment_num)
    print(f"Got Experiment:\n{experiment}")
    if experiment == None:
        #TODO: Throw an actual error here
        end_experiment(True)
        return

    axes = list(experiment.rotation_axis)
    #TODO: Add multi axis support
    if len(axes) > 1:
        print("Experiment with more than one axis not supported")
        end_experiment(True)
        return

    axis_map = {'X': 1, 'Y': 2, 'Z': 3}
    
    theta_d = experiment.angle

    hardware_startup(experiment)

    #TODO: better logging
    filename = f"{str(date.today())}_{str(time.localtime().tm_hour)}-{str(time.localtime().tm_min)}.csv"
    file = open(filename, "w")
    file.write("k, t[k], yaw[k], pitch[k], roll[k], dyawdt[k], dpitchdt[k], drolldt[k], ddyawdt2[k], ddpitchdt2[k], ddrolldt2[k], a, a, a, umotor[k], 0.0, 0.0, force[k 0], force[k 1], force[k 2], torque[k 0], torque[k 1], torque[k 2], theta[k], err[k], errdot[k], ecumul[k], u[k]\n")

    ########### MAIN CONTROL LOOP START ###########
    while (k < MAX_ITER):
        print(k)
        t[k]=time.time() - tstart
        dt=t[k] - t[k-1]
        
        # Get IMU data
        yaw[k],pitch[k],roll[k]=imu_data(imu,yaw0,yawOld)
        theta[k]=yaw[k]
        vel[k] = (theta[k]) - theta[k-1]/dt
        acc[k]=(vel[k] - vel[k-1])/dt
        err[k]=(theta[k] - theta_d)
        errdot[k]=(err[k] - err[k-1])/dt
        ecumul[k]=ecumul[k-1] + err[k]*dt

        [s,force[k,:],torque[k,:]] = sensor_read(bota_ft_sensor_driver)

        # Control Algorithm Using PID Controller
        u[k] = PID_control(theta_d, k, t, dt, I, J, theta, vel, acc, err, errdot, ecumul, kt0, kp0, kd0, ki0, torque[k,:])

        dyawdt[k]=(yaw[k] - yaw[k-1])/dt
        dpitchdt[k]=(pitch[k] - pitch[k-1])/dt
        drolldt[k]=(roll[k] - roll[k-1])/dt
        dyawdt[0]=0.0
        dpitchdt[0]=0.0
        drolldt[0]=0.0

        ddyawdt2[k]=(dyawdt[k] - dyawdt[k-1])/dt
        ddpitchdt2[k]=(dpitchdt[k] - dpitchdt[k-1])/dt
        ddrolldt2[k]=(drolldt[k] - drolldt[k-1])/dt

        #TODO: WRITE THIS TO A FILE
        print(f"k: {k}\nForce: {force[k]}\nTorque: {torque[k]}\n")
        a=0.0  # Linear acceleration a is not needed. Included here just for unuiformity of input/output files into SINDy. Linear acceleration a is not needed.

        
        # Write data for current timestep to log file 

        #Drive the Motor
        try:
            global SPINNING
            set_wheel_torque(axis_map[axes[0]], u[k])
            umotor[k] = read_data('TORQUE')[0][0]
            SPINNING = True
        except ERROR:
            end_experiment(True)
            
        #TODO: Update this for new motor
        time.sleep(0.025) # Good as of 11/5/2023 10:51 am

        if (k > 10): 
            meantheta=np.mean(theta[k-10:k])

        file.write("%5.0i, %4.3f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %10.2f, %10.2f, %10.2f, %10.2f, %10.2f\n" %  
            (k, t[k], 
            yaw[k], pitch[k], roll[k], 
            dyawdt[k], dpitchdt[k], drolldt[k], 
            ddyawdt2[k], ddpitchdt2[k], ddrolldt2[k], 
            a, a, a, 
            umotor[k], 0.0, 0.0, 
            force[k,0], force[k,1], force[k,2], 
            torque[k,0], torque[k,1], torque[k,2], 
            theta[k], err[k], errdot[k], ecumul[k], u[k]))

        yawOld=theta[k]
        k=k+1

    ########### MAIN CONTROL LOOP END ###########

    end_experiment()

start_experiment(1)