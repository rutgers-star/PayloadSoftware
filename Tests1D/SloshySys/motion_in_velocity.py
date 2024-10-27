# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 13:14:56 2023

@author: mfogel
"""

from ctypes import *
import time

def MotionInVelocity(keyhandle, NodeID, epos, umotor, acceleration):
    
    ret=0
    pErrorCode=c_uint()
    pDeviceErrorCode=c_uint()
    pVelocityIs=c_long() 
    pVelocityProfile=c_bool()
    umotor=c_long(int(umotor))
    acceleration=c_long(int(acceleration))
#    acceleration=c_unit(int(acceleration))


   
#    print("In MotionInVelocity")
#    print("acceleration = " , acceleration)
#    print("umotor = " , umotor)
#    print("epos = " , epos)
#    print("keyhandle = " , keyhandle)
#    print("NodeID = " , NodeID)

    
    # EXAMPLE    
    #ret = epos.VCS_SetVelocityProfile(keyhandle, NodeID, acceleration, acceleration, byref(pErrorCode))
    #EXAMPLE 

    ret = epos.VCS_ActivateProfileVelocityMode(keyhandle, NodeID, byref(pErrorCode) )

    ret = epos.VCS_SetVelocityProfile(keyhandle, NodeID, acceleration, acceleration, byref(pErrorCode))

    #EXAMPLE
    #ret= epos.VCS_ActivateProfileVelocityMode(keyhandle, NodeID, byref(pErrorCode) )
    #EXAMPLE
    #EXAMPLE from documentaton
    #BOOL VCS_MoveWithVelocity(HANDLE KeyHandle, WORD NodeId, long TargetVelocity, DWORD*pErrorCode)
    #EXAMPLE

    ret = epos.VCS_MoveWithVelocity(keyhandle, NodeID, umotor, byref(pErrorCode))

    #time.sleep(0.1)

    ret = epos.VCS_GetVelocityIs(keyhandle, NodeID, byref(pVelocityIs), byref(pErrorCode))
    #print('Velocity Device Code: %#5.8x' % pErrorCode.value)

    #BOOL VCS_GetVelocityIs(HANDLE KeyHandle, WORD NodeId, long* pVelocityIs, DWORD* pErrorCode)

    #DELETE LATER
    #pErrorCode=c_uint()    
    #ret=epos.VCS_SetDisableState(keyhandle, NodeID, byref(pErrorCode) )
    #print('Maxon Motor Device Disabled')
 
    # Close Com-Port
    #ret=epos.VCS_CloseDevice(keyhandle, byref(pErrorCode) )
    #print('Error Code Closing Port: %#5.8x' % pErrorCode.value)  
    #DELETE LATER

    Omega = pVelocityIs.value
    
    #print(type(pVelocityIs))
    #print(type(pVelocityIs.value))
    #print(type(Omega))
    #print("pVelocityIs = " , pVelocityIs)
    #print("pVelocityIs.value = " , pVelocityIs.value)
    #print("Omega = " , Omega)
    
#    print("Motor pVelocityIs = %i" % pVelocityIs.value)
#    print("Motor Omega  = %i" % Omega)
    
    return Omega