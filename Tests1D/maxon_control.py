#!/usr/bin/env python

"""
A module to start-up and shutdown the maxon motor for 1-Dimensional tests
"""

from ctypes import *

__author__="Mike Fogel"
__credits__=["Mike Fogel"]
__creation_date__="8/1/2023"

def init_maxon(epos):
    """
    Closes connection to and disables the Maxon Motor

    Args:
        epos (?): Easy to use POsitioning System - command library for Maxon

    Returns:
        key_handle (?): Open EPOS device controller 
        NodeID (int): Number associated to EPOS4 node ID setting 
    """
    # path='/opt/EposCmdLib_6.7.1.0/lib/v8/libEposCmd.so.6.7.1.0'
    # cdll.LoadLibrary(path)
    # epos=CDLL(path)
    
    # NodeID must match with hardware DIP switches setting of EPOS4
    NodeID=1


    pErrorCode=c_uint()
    pDeviceErrorCode=c_uint()
    
    # Open USB port
    print("Opening Maxon Motor USB Port...")
    key_handle=epos.VCS_OpenDevice(b'EPOS4', b'MAXON SERIAL V2', b'USB', b'USB0', byref(pErrorCode))
    
    if (key_handle != 0):
        # Verify error state
        ret=epos.VCS_GetDeviceErrorCode(key_handle, NodeID, 1, byref(pDeviceErrorCode), byref(pErrorCode))
        
        # Device Error Evaluation
        if (pDeviceErrorCode.value==0):
    
     		# Set Operation Mode PPM
            ret=epos.VCS_ActivateProfileVelocityMode(key_handle, NodeID, byref(pErrorCode) )
    
     		# Profile Velocity=500rpm / Acceleration=1000rpm/s / Deceleration=1000rpm/s
            ret=epos.VCS_SetVelocityProfile(key_handle, NodeID, -1000, 1000, byref(pErrorCode) )
            ret=epos.VCS_SetEnableState(key_handle, NodeID, byref(pErrorCode) )
            print('Maxon Motor Device Enabled')
    
        else:
            print('EPOS4 is in Error State: %#5.8x' % pDeviceErrorCode.value)
            print('EPOS4 Error Description can be found in the EPOS4 Fimware Specification')
    
     
    else:
        print('Could not open Maxon Motor USB-Port')
        print('key_handle: %8d' % key_handle)
        print('Error Openening Port: %#5.8x' % pErrorCode.value)
        
    return key_handle, NodeID

def close_maxon(key_handle, NodeID, epos):
    """
    Closes connection to and disables the Maxon Motor

    Args:
        key_handle (?): Open EPOS device controller 
        NodeID (int): Number associated to EPOS4 node ID setting 
        epos (?): Easy to use POsitioning System - command library for Maxon
    """

    pErrorCode=c_uint()    
    ret=epos.VCS_SetDisableState(key_handle, NodeID, byref(pErrorCode) )
    print('Maxon Motor Device Disabled')
    
    ret=epos.VCS_CloseDevice(key_handle, byref(pErrorCode) )