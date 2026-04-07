#!/usr/bin/env python

"""
A module which contains definitions for control algroithms to drive a motor for the 1.D. tests of the SPICEsat
"""

import math
import numpy as np 

author="Mike Fogel"
credits=["Mike Fogel"]
creation_date="2024"

#TODO: docustring
def PID_control(theta_d, k, t, dt, I, J, theta, vel, acc, err, errdot, ecumul, kt, kp, kd, ki, torque):

    torquez = torque[2]
    ucontrol = (I/J)*(kp*err[k] + kd*errdot[k] + ki*ecumul[k])*(60/2*math.pi) - torquez

    return ucontrol