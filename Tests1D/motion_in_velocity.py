#!/usr/bin/env python

"""
A module which calculates the current velocity of the Maxon Motor
"""

from ctypes import *
import time

__author__="Mike Fogel"
__credits__=["Mike Fogel"]
__creation_date__="8/5/2023"

__version__="1.0.0"
__maintainer__="Mike Fogel"
__email__="mikefogelny@gmail.com"
__status__="Development"

def MotionInVelocity(keyhandle, NodeID, epos, umotor, acceleration):
    """
    Calculates the current velocity of the Maxon Motor

    Args:
        key_handle (?): Open EPOS device controller 
        NodeID (int): Number associated to EPOS4 node ID setting 
        epos (?): Easy to use POsitioning System - command library for Maxon
        umotor (float): current speed of the motor in RPM
        acceleration (float): current acceleration of the motor in RPM/s
    """
    
    ret=0
    pErrorCode=c_uint()
    pDeviceErrorCode=c_uint()
    pVelocityIs=c_long() 
    pVelocityProfile=c_bool()
    umotor=c_long(int(umotor))
    acceleration=c_long(int(acceleration))

    ret = epos.VCS_ActivateProfileVelocityMode(keyhandle, NodeID, byref(pErrorCode) )

    ret = epos.VCS_SetVelocityProfile(keyhandle, NodeID, acceleration, acceleration, byref(pErrorCode))

    ret = epos.VCS_MoveWithVelocity(keyhandle, NodeID, umotor, byref(pErrorCode))

    ret = epos.VCS_GetVelocityIs(keyhandle, NodeID, byref(pVelocityIs), byref(pErrorCode))
    
    Omega = pVelocityIs.value

    return Omega