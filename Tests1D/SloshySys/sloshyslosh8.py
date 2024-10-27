# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 09:26:28 2023

@author: mfogel
"""



import math
import numpy as np 
import matplotlib.pyplot as plt
import time
from init_imu import init_imu
from imudata import imudata
from init_maxon import init_maxon
from plotsloshy import plotsloshy
from plotsloshy2 import plotsloshy2
from plotsloshy3 import plotsloshy3
from motion_in_velocity import MotionInVelocity
from close_maxon import close_maxon
from ctypes import *
import subprocess

# theta = platform angle
# vel = platform angular velocity
# acc = platform angular acceleration
# u = RPM calculated for motor
# umotor = RPM commanded to motor
# Omega = RPM measured from motor


maxiter=100 # Max number of allowed iterations to meet desired angle 
amax=10000 # Max RPM of the maxon motor. SAFETY stop. 3500 is allowable.
vmax=3000 # Max RPM of the maxon motor. SAFETY stop. 3500 is allowable.
umax=amax
acceleration0=4000

    

# Reaction wheel MoI
Jx=2.491E-4 # kg m^2
Jy=2.250E-4 # kg m^2
Jz=4.703E-4 # kg m^2
J=math.sqrt(Jx**2 + Jy**2 + Jz**2)
I = 0.02344 # Full
#I = 234E-4  # Full
#I = 0.01180  #Empty
#I = 118.0E-4 # Empty

# Initialization
theta_d=90 #Desired angle
tol=0.5  # Tolerance to angle reaching desired angle

#kp0=5.5;
#kp0=0.011 
#kd0=0.01
#ki0=0.001

#Somewhat there as of 12/20/23
#kp0=0.005 
#kd0=0.0001
#ki0=0.0001

#Somewhat there as of 12/20/23
#kp0=0.0055 
#kd0=0.001
#ki0=0.001

#Somewhat there as of 12/20/23
kp0=0.0045 
kd0=0.0015
ki0=0.001

#Very close there as of 12/28/23
kp0=0.0075 
kd0=0.0015
ki0=0.001



# Freqency Response
wn=math.sqrt(kp0/I)
eta=kd0/(2*I*wn)
p = [1, 2*eta*wn, wn**2]
r = np.roots(p)
#print('wn      = natural freq = {0:.4f} '.format(wn))
#print('eta     = eta          = {0:.4f} '.format(eta))
#print('roots   = roots        = \n',r)


########### PRESSURE SENSOR STARTUP CODE BEGIN ##############



########### PRESSURE SENSOR STARTUP CODE END ##############


########### MOTOR STARTUP CODE BEGIN ##############
# Folder created for example: /home/pi/src/python/
# Copy maxon motor Linux Library arm v7 into this folder
# Library must match according your cpu, eg. PI3 has arm v7
# Library must match according your cpu, eg. PI3 has arm v7
# Library must match according your cpu, eg. PI4 has arm v8  # Fogel added 6/25/2023
# EPOS Comand Library can be found here, when EPOS Studio has been installed:
# path="C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS4\04 Programming\Linux Library"
# path='/home/pi/src/python/libEposCmd.so.6.6.2.0'
# From working version  path='/opt/EposCmdLib_6.7.1.0/lib/v8/libEposCmd.so.6.7.1.0'
path='/opt/EposCmdLib_6.7.1.0/lib/v8/libEposCmd.so.6.7.1.0' # If Linux
#path='.\EposCmd64.dll'  # If WINDOWS
cdll.LoadLibrary(path)
epos=CDLL(path)
#NodeID must match with hardware DIP switches setting of EPOS4
#NodeID=1
#keyhandle=0
# Define return variables from EPOS library functions
ret=0
pErrorCode=c_uint()
pDeviceErrorCode=c_uint()
pVelocityIs=c_long()
keyhandle,NodeID = init_maxon(epos)
########### MOTOR STARTUP CODE END ##############

########### IMU STARTUP CODE BEGIN ##############
yaw0,imu = init_imu()
yawOld=0
print('Yaw0:',yaw0)
#print('YawOld:',yawOld)
#print('IMU Port:',imu)
########### IMU STARTUP CODE END ##############

########### CAMERA STARTUP CODE BEGIN ##############
print("Staring camera")
camlog=open("camlog.txt",'w')
#cam=subprocess.Popen(["/usr/local/bin/libcamera-vid", "-t 20000", "--nopreview", "--width", "640", "--height","480","--vflip","--saturation","0","--save-pts","camtimes.txt","--codec","mjpeg","--exposure","long","--framerate","24","-o","test.mjpeg"], text=True, stderr=camlog)
cam=subprocess.Popen(["/usr/local/bin/libcamera-vid", "-t 20000", "--nopreview", "--width", "960", "--height","540","--vflip","--saturation","0","--save-pts","camtimes.txt","--exposure","long","--framerate","24","-o","sloshing.h264"], text=True, stderr=camlog)
print("Camera started")
########### CAMERA STARTUP CODE END ##############


k=1
t = np.empty(maxiter)
theta = np.empty(maxiter)
vel = np.empty(maxiter)
acc = np.empty(maxiter)
Omega = np.empty(maxiter)
err = np.empty(maxiter)
errdot = np.empty(maxiter)
ecumul = np.empty(maxiter)
u = np.empty(maxiter)
umotor = np.empty(maxiter)
meantheta=0
t[0]=0
#err[0]=-theta_d
err[0]=0
err[1]=0
errdot[0]=0
errdot[1]=0
ecumul[0]=0
ecumul[1]=0
tstart=time.time()
#time.sleep(1.0E-16)

##### MAIN CONTROL LOOP ####
#while (k <= maxiter-1) and abs(meantheta - theta_d) > tol):
while (k < maxiter):
    t[k]=time.time() - tstart
    dt=t[k] - t[k-1]
#    print('Iteration #        = {0:4d} {1:4f} '.format(k,t[k]))
#    time.sleep(1.0E-14)
    
# Get IMU data
    yaw,pitch,roll=imudata(imu,yaw0,yawOld)

    theta[k]=yaw
    vel[k] = (theta[k]) - theta[k-1]/dt
    acc[k]=(vel[k] - vel[k-1])/dt

    err[k]=(theta[k] - theta_d)
    errdot[k]=(err[k] - err[k-1])/dt
    ecumul[k]=ecumul[k-1] + err[k]*dt
    
    kp=kp0;kd=kd0;ki=ki0;

    # Control Algorithm Using PID Controller
    u[k] = (I/J)*(kp*err[k] + kd*errdot[k] + ki*ecumul[k])*(60/2*math.pi) 

    umotor[k]=u[k];
    acceleration=abs(umotor[k])
    if acceleration > amax:
        acceleration=amax

    velocity=np.sign(u[k])*vmax


# Drive the Motor
#    acceleration=abs(umotor[k])
#    acceleration=(umotor[k])
#    vmax=-vmax

#    if ((k == 1) or (k % 5 == 0)):
    Omega[k] = MotionInVelocity(keyhandle, NodeID, epos, velocity, acceleration)
#    time.sleep(0.05) # Good as of 11/5/2023 10:51 am
    time.sleep(0.025) # Good as of 11/5/2023 10:51 am

#    move = MotionInVelocity(keyhandle, NodeID, epos, velocity, acceleration)
#    move = epos.VCS_GetVelocityIs(keyhandle, NodeID, byref(pVelocityIs), byref(pErrorCode))
#    Omega[k] = pVelocityIs.value
    
#    print("%5.0i    %4.3f  %10.2f  %10.2f %10.2f %10.2f %10.2f %10.2f %10.2f " % (k,t[k], theta[k], err[k], errdot[k], ecumul[k], umotor[k], u[k], Omega[k-1]))
    print("%5.0i    %4.3f  %10.2f  %10.2f %10.2f %10.2f %10.2f %10.2f " % (k,t[k], theta[k], err[k], errdot[k], ecumul[k], umotor[k], u[k]))
#    print(k,t[k], theta[k], meantheta, err[k], errdot[k], ecumul[k], u[k])
#    print(k,t[k], dt, theta[k], theta[k-1], vel[k])


    if (k > 10): 
        meantheta=np.mean(theta[k-10:k])

    yawOld=theta[k]
    k=k+1

errdot[0]=0
errdot[1]=0
u[0]=0
u[1]=0
umotor[0]=0
umotor[1]=0



print("End of MAIN LOOP")    
print("Shutting Motor Down")    
close_maxon(keyhandle,NodeID, epos)
print("Motor Stopped")    

print("Closing Camera File")
print("Video file output: sloshing.h264")
camlog.close()
print("Camera Closed")

print("Plotting")    
#
plotsloshy3(t, theta, theta_d, u, umotor, umax, Omega, vel, acc, err, errdot, ecumul)
#plt.show(block=False)
plt.show()


print("End of CODE")  
