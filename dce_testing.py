#!/usr/bin/env python

"""
A module written to to test custom BCT DCE control code
"""

from Logs.log import log
from dce_control import *
from time import sleep

__author__="Simon Kowerski"
__credits__=["Simon Kowerski"]
__creation_date__="8/8/2024"


"""
Objectives for 10/25
confirm startup sequence works
confirm all commands work
Read commanded speed and torque to find the maximums for our wheel
"""

spin = True

try:
    log(0)
    startup()

    if spin:
        set_wheel_torque(1, 1)
        sleep(5)

    output=read_data("TORQUE")

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
    
    log(1)

except ERROR:
    if spin:
        set_wheel_speed(1, 0)
    log(2)
