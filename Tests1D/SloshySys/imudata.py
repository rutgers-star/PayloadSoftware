# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 17:05:25 2023

@author: mfogel
"""

import serial
import math
import numpy as np 

pi=math.pi

# function definition
def imudata(imu,yaw0,yawOld):
#    print("Reading IMU")

    data = imu.readline()
    numData=data.decode()
    numData = numData.split(",")
    numData = np.array(numData[0:3], dtype=float)
    q1=numData[0]
    q2=numData[1]
    q3=numData[2]

    
    q0 = (math.sqrt(abs(( 1.0 - ((q1     * q1    ) + (q2     * q2    ) + (q3     * q3     ))))));
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
    yawNew = yawNew - yaw0
    if yawNew < 0 and yawOld > 90:
        yawNew=yawNew+360;


#    print(yawNew, pitchNew, rollNew)   


    return yawNew, pitchNew, rollNew