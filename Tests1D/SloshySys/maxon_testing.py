# -*- coding: utf-8 -*-
import math
import time
import numpy as np 
from init_maxon import init_maxon
from motion_in_velocity import MotionInVelocity
from close_maxon import close_maxon
from ctypes import *

maxiter = 3 # Max number of allowed iterations to meet desired angle 
   

# Reaction wheel MoI
Jx=2.491E-4 # kg m^2
Jy=2.250E-4 # kg m^2
Jz=4.703E-4 # kg m^2
J=math.sqrt(Jx**2 + Jy**2 + Jz**2)
#I = 0.02344 # Full
#I = 234E-4  # Full
I = 0.01180  #Empty
#I = 118.0E-4 # Empty


#kp0=5.5;
kp=0.1 
kd=0.000
ki=0.000

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

k=1
Omega = np.empty(maxiter)
u = np.empty(maxiter)
err = np.empty(maxiter)

amax=4000 # Max RPM of the maxon motor. SAFETY stop. 3500 is allowable.
vmax=2500 # Max RPM of the maxon motor. SAFETY stop. 3500 is allowable.
acceleration=amax
vmax=vmax

##### MAIN CONTROL LOOP ####
print("Start of MAIN LOOP")    
while (k < maxiter):
#    u[k] = (I/J)*(-kp*err[k] + -kd*errdot[k] + -ki*ecumul[k])*(60/2*math.pi)
    u[k] = (I/J)*(-kp*err[k])*(60/2*math.pi)
    Omega[k]=MotionInVelocity(keyhandle, NodeID, epos, vmax, acceleration)
    print("%5.0i    %10.2f  %10.2f  %10.2f  %10.2f  " % (k, err[k], u[k], vmax, acceleration))
    time.sleep(5)
#    print("REVERSING acceleration")
#    acceleration=-amax
    print("REVERSING velocity")
    vmax=-vmax
    k=k+1
        
print("End of MAIN LOOP")    

print("Shutting Motor Down")    
close_maxon(keyhandle,NodeID, epos)

print("End of CODE")  
