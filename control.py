# -*- coding: utf-8 -*-
#TODO: Format
"""
Created on Mon Aug 26 10:37:52 2024

@author: mfogel
"""

import math
import numpy as np 

# function definition
def PID_control(theta_d, k, t, dt, I, J, theta, vel, acc, err, errdot, ecumul):    
    kp=0.011 
    kd=0.01
    ki=0.001
    
    ucontrol = (I/J)*(kp*err[k] + kd*errdot[k] + ki*ecumul[k])*(60/2*math.pi) 

    return ucontrol