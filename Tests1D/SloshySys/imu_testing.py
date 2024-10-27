# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 09:00:00 2023

@author: mfogel
"""

#import serial.tools.list_ports as port_list

import serial
import time
import numpy as np
import math
from matplotlib import pyplot as plt


baud=115200
header=15
maxt=200
settled=0
imutol=1.0E-6
qOLD=100
pi=math.pi

#fig, ax = plt.subplots()

#ports = list(serial.tools.list_ports.comports())
#for p in ports:
#    print (p)


#imu = serial.Serial('COM5',baud)
imu = serial.Serial('/dev/ttyUSB1',baud, timeout = 5)

print("Clearing IMU Header")
for i in range(0,header):
        data = imu.readline()
#        print(i,data)

i=0
tstart=time.time()
print("Settling IMU...")
while (settled == 0) and (i < maxt):
    i=i+1
    t=time.time() - tstart
    data = imu.readline()
    numData=data.decode()
    numData = numData.split(",")
    numData = np.array(numData[0:3], dtype=float)
    q1=numData[0]
    q2=numData[1]
    q3=numData[2]
#    print(i,q1,q2,q3)
    q0 = math.sqrt(abs(( 1.0 - ((q1     * q1    ) + (q2     * q2    ) + (q3     * q3     )))))
    q2sqr = (q2 * q2)


    #roll calculation from parameters
    t0 = (+2.0 * (q0 * q1 + q2 * q3))
    t1 = (+1.0 - 2.0 * (q1 * q1 + q2sqr))
    rollNew = (math.atan2(t0, t1) * 180.0 / pi)
 
    #pitch calculation using euler parameters
    t2 = (+2.0 * (q0 * q2 - q3 * q1))
    if t2 >= 1:
        pitchNew = float(90)
    elif t2<= -1:
        pitchNew = float(-90)
    else:
        pitchNew = float(math.asin(t2) * 180.0 / pi)
        
    #yaw calculation
    t3 = float(+2.0 * (q0 * q3 + q1 * q2))
    t4 = float(+1.0 - 2.0 * (q2sqr + q3 * q3))
    yawNew = float(math.atan2(t3, t4) * 180.0 / pi)
    yaw0=yawNew


#    print(i,yawNew, pitchNew, rollNew)    

#    plot stuff
#    ax.scatter(t,rollNew,color='r')
#    ax.scatter(t,pitchNew,color='g')
#    ax.scatter(t,yawNew,color='b')
#    ax.set_ylim([-90,90])
#    ax.set_xlim([0,120])
#    # drawing updated values
#    fig.canvas.draw()
#    # This will run the GUI event
#    # loop until all UI events
#    # currently waiting have been processed
#    fig.canvas.flush_events()

    
    if ((abs(q0 - qOLD) < imutol) and settled == 0):
        print("IMU Settled t = ",t)
        print("IMU Settled yaw0 = ",yaw0)
        settled=1;
        tsettle=t;

    qOLD=q0;