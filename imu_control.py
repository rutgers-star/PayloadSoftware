#!/usr/bin/env python

"""
A module to control and access the IMU & Data for 1-Dimensional Tests
"""

import serial
import math
import time
import numpy as np 
from matplotlib import pyplot as plt
import serial.tools.list_ports
from Logs.log import log
from Logs.errors import ERROR 

__author__="Mike Fogel"
__credits__=["Mike Fogel", "Simon Kowerski"]
__creation_date__="7/25/2023"

pi=math.pi

#TODO: maybe redo how this works, make it more similar to dce control module

def init_imu():
    """
    Initialize the IMU to allow collection of data

     Returns
        yaw0 (int): initial yaw
        imu (imu): conection to the connected imu device

    Raises
        ERROR(1350): Failed to initalize IMU

    """

    log(350)

    baud=115200
    header=15
    maxt=200
    settled=0
    imutol=1.0E-6
    qOLD=100

    try:
        ports=serial.tools.list_ports.comports()
        imu=serial.Serial(ports[0].device,baud, timeout=5)
    except Exception:
        raise ERROR(1350, "failed to open serial connection")

    # Clearing IMU Header
    for i in range(0,header):
        data=imu.readline()
    
    # Settling IMU
    i=0
    tstart=time.time()
    while (settled == 0) and (i < maxt):
        i=i+1
        t=time.time() - tstart
        data=imu.readline()
        numData=data.decode()
        numData=numData.split(",")
        numData=np.array(numData[0:3], dtype=float)
        q1=numData[0]
        q2=numData[1]
        q3=numData[2]
        q0=math.sqrt(abs(( 1.0 - ((q1     * q1    ) + (q2     * q2    ) + (q3     * q3     )))))
        q2sqr=(q2 * q2)
    
    
        # roll calculation from parameters
        t0=(+2.0 * (q0 * q1 + q2 * q3))
        t1=(+1.0 - 2.0 * (q1 * q1 + q2sqr))
        rollNew=(math.atan2(t0, t1) * 180.0 / pi)
     
        # pitch calculation using euler parameters
        t2=(+2.0 * (q0 * q2 - q3 * q1))
        if t2 >= 1:
            pitchNew=float(90)
        elif t2<= -1:
            pitchNew=float(-90)
        else:
            pitchNew=float(math.asin(t2) * 180.0 / pi)
            
        # yaw calculation
        t3=float(+2.0 * (q0 * q3 + q1 * q2))
        t4=float(+1.0 - 2.0 * (q2sqr + q3 * q3))
        yawNew=float(math.atan2(t3, t4) * 180.0 / pi)
        yaw0=yawNew
        
        if ((abs(q0 - qOLD) < imutol) and settled == 0):
            log(1352, f"t= {t}, yaw0= {yaw0}")
            settled=1;
            tsettle=t;
    
        qOLD=q0;
       
    if (settled == 0):
        raise ERROR(1350, "IMU did not settle")

    return yaw0, imu

def imu_data(imu, yaw0, yawOld):
    """
    Collects and returns data from the connected IMU Unit

    Args:
        imu (imu): variable of connection to the connected imu device
        yaw0 (int): the first yaw value stored
        yawOld (int): the previous yaw value stored

    Returns:
        int[]: yawNew, pitchNew, rollNew - self explanatory
    """
    log(351)
    data=imu.readline()
    numData=data.decode()
    numData=numData.split(",")
    numData=np.array(numData[0:3], dtype=float)
    q1=numData[0]
    q2=numData[1]
    q3=numData[2]

    
    q0=(math.sqrt(abs(( 1.0 - ((q1     * q1    ) + (q2     * q2    ) + (q3     * q3     ))))));
    q2sqr=(q2 * q2)

    # roll calculation from parameters
    t0=(+2.0 * (q0 * q1 + q2 * q3))
    t1=(+1.0 - 2.0 * (q1 * q1 + q2sqr))
    rollNew=(math.atan2(t0, t1) * 180.0 / pi)

    # pitch calculation using euler parameters
    t2=(+2.0 * (q0 * q2 - q3 * q1))
    if t2 >= 1:
        pitchNew=float(90)
    elif t2<= -1:
        pitchNew=float(-90)
    else:
        pitchNew=float(math.asin(t2) * 180.0 / pi)

    # yaw calculation
    t3=float(+2.0 * (q0 * q3 + q1 * q2))
    t4=float(+1.0 - 2.0 * (q2sqr + q3 * q3))
    yawNew=float(math.atan2(t3, t4) * 180.0 / pi)
    yawNew=yawNew - yaw0
    if yawNew < 0 and yawOld > 90:
        yawNew=yawNew+360;

    return yawNew, pitchNew, rollNew