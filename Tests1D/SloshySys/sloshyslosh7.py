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
umax=2500 # Max RPM of the maxon motor. SAFETY stop. 3500 is allowable.
acceleration0=4000

    

# Reaction wheel MoI
Jx=2.491E-4 # kg m^2
Jy=2.250E-4 # kg m^2
Jz=4.703E-4 # kg m^2
J=math.sqrt(Jx**2 + Jy**2 + Jz**2)
#I = 0.02344 # Full
#I = 234E-4  # Full
I = 0.01180  #Empty
#I = 118.0E-4 # Empty

# Initialization
theta_d=90 #Desired angle
tol=2  # Tolerance to angle reaching desired angle

#kp0=5.5;
kp0= 1.5
kd0=0.1 
ki0=0.00

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
#os.system("libcamera-vid -t 10000  --nopreview --width 640 --height 480 --sharpness 1.5 --exposure long --framerate 5 --codec mjpeg -o test.mjpeg")
#os.system("libcamera-vid -t 10000   --width 640 --height 480 --sharpness 1.5 --exposure long --framerate 5 --codec mjpeg -o test.mjpeg &",stdout="camlog.txt",stderr=STDOUT)
#subprocess.run("libcamera-vid -t 10000   --width 640 --height 480 --sharpness 1.5 --exposure long --framerate 5 -o test.h264 > camlogos.txt &",stdout="camlog.txt",stderr=stdout)
#camlog=subprocess.run(["libcamera-vid", "-t 10000", "--width 640", "--height 480", "--sharpness 1.5", "--exposure long", "--framerate 5", "-o test.h264," "> camlogos.txt," "&"], capture_output=True)
#camlog=subprocess.run(["libcamera-vid -t 10000 --width 640 --height 480 --vflip --sharpness 1.5 --exposure long --framerate 5 -o test.h264 &"], capture_output=True)
#camlog=subprocess.run(["libcamera-vid", "-t 15000", "--width", "640", "--height","480","--vflip","--sharpness","1.5","--exposure","long","--framerate","5","-o","test.h264"], capture_output=True, text=True)
print("Staring camera")
camlog=open("camlog.txt",'w')
#cam=subprocess.Popen(["/usr/local/bin/libcamera-vid", "-t 20000", "--width", "640", "--height","480","--vflip","--sharpness","1.5","--exposure","long","--framerate","5","-o","test.h264"], text=True, stderr=camlog)
#cam=subprocess.Popen(["/usr/local/bin/libcamera-vid", "-t 20000", "--nopreview", "--width", "640", "--height","480","--vflip","--saturation","0","--exposure","long","--framerate","5","-o","test.h264"], text=True, stderr=camlog)
cam=subprocess.Popen(["/usr/local/bin/libcamera-vid", "-t 20000", "--nopreview", "--width", "640", "--height","480","--vflip","--saturation","0","--save-pts","camtimes.txt","--codec","mjpeg","--exposure","long","--framerate","10","-o","test.mjpeg"], text=True, stderr=camlog)
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
err[0]=-theta_d
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
    
          
    if abs(err[k]) < 5:
        print("Reduce Acceleration - by 100")
        acceleration=acceleration0*0.01
    elif abs(err[k]) < 10:
        print("Reduce Acceleration - by 10\n")
        acceleration=acceleration0*0.1
    elif abs(err[k]) < 15:
        print("Reduce Acceleration - by 1/2\n")
        acceleration=acceleration0*0.5
    else:
        acceleration=acceleration0;

    kp=kp0;kd=kd0;ki=ki0;    

    # Control Algorithm Using PID Controller
    u[k] = (I/J)*(kp*err[k] + kd*errdot[k] + ki*ecumul[k]); 

    umotor[k]=u[k];
    if abs(u[k]) > umax:
        umotor[k]=np.sign(u[k])*umax;
        
   # Drive the Motor
#    if (k % 10 == 0):
#    if ((k == 1) or (k % 10 == 0)):
#        print("Driving motor with umotor = " % umotor[k])
#        print("Driving motor with umotor = {0:4d} {1:4f} ".format(k,umotor[k]))
    Omega[k]=MotionInVelocity(keyhandle, NodeID, epos, umotor[k], acceleration)
#    ret = epos.VCS_GetVelocityIsAveraged(keyhandle, NodeID, byref(pVelocityIs), byref(pErrorCode))
#    Omega[k]=pVelocityIs.value

#    print("%5.0i    %4.3f  %10.2f  %10.2f %10.2f %10.2f %10.2f %10.2f %10.2f " % (k,t[k], theta[k], err[k], errdot[k], ecumul[k], umotor[k], u[k], Omega[k-1]))
    print("%5.0i    %4.3f  %10.2f  %10.2f %10.2f %10.2f %10.2f %10.2f " % (k,t[k], theta[k], err[k], errdot[k], ecumul[k], umotor[k], u[k]))
#    print(k,t[k], theta[k], meantheta, err[k], errdot[k], ecumul[k], u[k])
#    print(k,t[k], dt, theta[k], theta[k-1], vel[k])


    if (k > 10):
        meantheta=np.mean(theta[k-10:k])

    yawOld=theta[k]
    k=k+1

print("End of MAIN LOOP")    
print("Shutting Motor Down")    
close_maxon(keyhandle,NodeID, epos)

print("Closing Camera File")
camlog.close()

print("Plotting")    
#
plotsloshy(t, theta, theta_d, u, umotor, umax, Omega, vel, acc, err, errdot, ecumul)
#plt.show(block=False)
plt.show()


print("End of CODE")  
