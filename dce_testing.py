#!/usr/bin/env python

#TODO: Update docustring
"""
A module written to to test custom BCT DCE control code
"""

from Logs.log import log
from dce_control import *
from time import sleep
from imu_control import *

__author__="Simon Kowerski"
__credits__=["Simon Kowerski"]
__creation_date__="8/8/2024"

spin = True
spinning = False        # Keeps track of if the wheel is currently spinninng. Should be false at compile time
kill = False            # If set to true, will simply connect to the wheel and set its speed to zero and then end

imu_data_points = 80    # Number of times to read and print imu data for each direction
time_each_dir = 20      # Time delay (in seconds) before switching wheel torque

__gExpLogPath="Logs/ExpLogs/"

try:
    log(0)
    dce_startup()

    filename = f"{__gExpLogPath}experiment-timesteps.log"
    file = open(filename, "w")

    if kill:
        set_wheel_speed(1,0)


    else:
        global yaw0, imu, yawOld
        yaw0,imu=init_imu()
        yawOld=0
    
        if spin:
            set_wheel_torque(1,1)
            spinning = True
            print("Full Positive Torque")
            for i in range(imu_data_points):
                yaw,pitch,roll=imu_data(imu,yaw0,yawOld)
                file.write(f"{i} yaw: {yaw}\tpitch: {pitch}\troll: {roll}\n")
                sleep(time_each_dir/imu_data_points)

            set_wheel_torque(1,-1)
            print("\nFull Negative Torque")
            for x in range(imu_data_points):
                yaw,pitch,roll=imu_data(imu,yaw0,yawOld)
                file.write(f"{x} yaw: {yaw}\tpitch: {pitch}\troll: {roll}\n")
                sleep(time_each_dir/imu_data_points)


        output=read_data("Torque")

        print("torque")
        print(output[0])
        print(output[1])
        print(output[2])
        print()

        output=read_data("SPEED")

        print("speed")
        print(output[0])
        print(output[1])
        print(output[2])
        print()

    if spin:
        set_wheel_speed(1, 0)
        spinning = False

    log(1)

except ERROR:
    if spin and spinning:
        set_wheel_speed(1, 0)
    log(2)

except Exception:
    if spin and spinning:
        set_wheel_speed(1, 0)
    raise ERROR(1000)