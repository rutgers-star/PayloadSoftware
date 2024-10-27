#!/usr/bin/env python

"""
A module to run a 1-Dimensional test bench of the S.T.A.R. SPICEsat

Atributes:
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
from maxon_control import init_maxon, close_maxon
from plot_tools import plot_sloshy
from motion_in_velocity import MotionInVelocity

__author__="Mike Fogel"
__credits__=["Mike Fogel"]
__creation_date__="7/2/2023"

MAX_ITER=100        # Max number of allowed iterations to meet desired angle 
MAX_ACCEL=10000     # Max acceleration in RPM/s of the maxon motor. SAFETY stop.
MAX_VEL=3000        # Max RPM of the maxon motor. SAFETY stop. 3500 is allowable.

########### INITIAL VALUE CALCULATIONS START ###########
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




########### PRESSURE SENSOR STARTUP CODE END ##############

########### MOTOR STARTUP CODE BEGIN ###########
# Folder created for example: /home/pi/src/python/
# Copy maxon motor Linux Library arm v7 into this folder
# Library must match according your cpu, eg. PI4 has arm v8  # Fogel added 6/25/2023
# EPOS Comand Library can be found here, when EPOS Studio has been installed:
# path="C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS4\04 Programming\Linux Library"
# path='/home/pi/src/python/libEposCmd.so.6.6.2.0'
# From working version  path='/opt/EposCmdLib_6.7.1.0/lib/v8/libEposCmd.so.6.7.1.0'
path='/opt/EposCmdLib_6.7.1.0/lib/v8/libEposCmd.so.6.7.1.0' # If Linux
cdll.LoadLibrary(path)
epos=CDLL(path)
# Define return variables from EPOS library functions
ret=0
pErrorCode=c_uint()
pDeviceErrorCode=c_uint()
pVelocityIs=c_long()
# Initalize EPOS
key_handle,NodeID=init_maxon(epos)
########### MOTOR STARTUP CODE END ###########

########### IMU STARTUP CODE BEGIN ###########
yaw0,imu=init_imu()
yawOld=0
print('Yaw0:',yaw0)
########### IMU STARTUP CODE END ###########

########### CAMERA STARTUP CODE BEGIN ###########
print("Staring camera")
camlog=open("camlog.txt",'w')
cam=subprocess.Popen(["/usr/local/bin/libcamera-vid", "-t 20000", "--nopreview", "--width", "960", "--height","540","--vflip","--saturation","0","--save-pts","camtimes.txt","--exposure","long","--framerate","24","-o","sloshing.h264"], text=True, stderr=camlog)
print("Camera started")
########### CAMERA STARTUP CODE END ###########

########### MAIN CONTROL LOOP START ###########
while (k < MAX_ITER):
    t[k]=time.time() - tstart
    dt=t[k] - t[k-1]

    # Get IMU data
    yaw,pitch,roll=imu_data(imu,yaw0,yawOld)

    theta[k]=yaw
    vel[k]=(theta[k]) - theta[k-1]/dt
    acc[k]=(vel[k] - vel[k-1])/dt

    err[k]=(theta[k] - theta_d)
    errdot[k]=(err[k] - err[k-1])/dt
    ecumul[k]=ecumul[k-1] + err[k]*dt
    
    kp=kp0
    kd=kd0 
    ki=ki0

    # Control Algorithm Using PID Controller
    u[k]=(I/J)*(kp*err[k] + kd*errdot[k] + ki*ecumul[k])*(60/2*math.pi) 

    umotor[k]=u[k];
    acceleration=abs(umotor[k])
    if acceleration > MAX_ACCEL:
        acceleration=MAX_ACCEL

    velocity=np.sign(u[k])*MAX_VEL


    # Drive the Motor
    Omega[k]=MotionInVelocity(key_handle, NodeID, epos, velocity, acceleration)
    time.sleep(0.025) # Good as of 11/5/2023 10:51 am
    
    print("%5.0i    %4.3f  %10.2f  %10.2f %10.2f %10.2f %10.2f %10.2f " % (k,t[k], theta[k], err[k], errdot[k], ecumul[k], umotor[k], u[k]))

    if (k > 10): 
        meantheta=np.mean(theta[k-10:k])

    yawOld=theta[k]
    k=k+1
########### MAIN CONTROL LOOP END ###########

errdot[0]=0
errdot[1]=0
u[0]=0
u[1]=0
umotor[0]=0
umotor[1]=0

print("End of MAIN LOOP")    
print("Shutting Motor Down")    
close_maxon(key_handle,NodeID, epos)
print("Motor Stopped")    

print("Closing Camera File")
print("Video file output: sloshing.h264")
camlog.close()
print("Camera Closed")

print("Plotting")
plot_sloshy(t, theta, theta_d, u, umotor, MAX_ACCEL, Omega, vel, acc, err, errdot, ecumul)
plt.show()


print("End of CODE")  
