# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 16:33:23 2023

@author: mfogel
"""

#import serial
#import time
from ctypes import *

# Folder created for example: /home/pi/src/python/
# Copy maxon motor Linux Library arm v7 into this folder
# Library must match according your cpu, eg. PI3 has arm v7
# Library must match according your cpu, eg. PI3 has arm v7
# Library must match according your cpu, eg. PI4 has arm v8  # Fogel added 6/25/2023
# EPOS Comand Library can be found here, when EPOS Studio has been installed:
# C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS4\04 Programming\Linux Library
# path='/home/pi/src/python/libEposCmd.so.6.6.2.0'
# From working version  path='/opt/EposCmdLib_6.7.1.0/lib/v8/libEposCmd.so.6.7.1.0'


# function definition
def init_maxon(epos):
#    path='/opt/EposCmdLib_6.7.1.0/lib/v8/libEposCmd.so.6.7.1.0'
#    cdll.LoadLibrary(path)
#    epos=CDLL(path)
    
#NodeID must match with hardware DIP switches setting of EPOS4
    NodeID=1
#    keyhandle=0
    # Define return variables from EPOS library functions
#    ret=0
#    pErrorCode=c_uint()
#    pDeviceErrorCode=c_uint()

    pErrorCode=c_uint()
    pDeviceErrorCode=c_uint()
    
    #Open USB port
    print("Opening Maxon Motor USB Port...")
    keyhandle=epos.VCS_OpenDevice(b'EPOS4', b'MAXON SERIAL V2', b'USB', b'USB0', byref(pErrorCode))
    #GOOD    keyhandle=epos.VCS_OpenDevice(b'EPOS4', b'MAXON SERIAL V2', b'USB', b'USB0', byref(pErrorCode) )
    
    if (keyhandle != 0):
#        print('Keyhandle: %8d' % keyhandle)
        #Verify error state
        ret=epos.VCS_GetDeviceErrorCode(keyhandle, NodeID, 1, byref(pDeviceErrorCode), byref(pErrorCode))
#        print('Device Error: %#5.8x' % pDeviceErrorCode.value)
        
        #Device Error Evaluation
        if (pDeviceErrorCode.value==0):
    
     		# Set Operation Mode PPM
            ret=epos.VCS_ActivateProfileVelocityMode(keyhandle, NodeID, byref(pErrorCode) )
    
     		# Profile Velocity=500rpm / Acceleration=1000rpm/s / Deceleration=1000rpm/s
            ret=epos.VCS_SetVelocityProfile(keyhandle, NodeID, -1000, 1000, byref(pErrorCode) )
    
     		# Read Position Actual Value with VCS_GetObject()
            #ret=GetPosition()
    
            ret=epos.VCS_SetEnableState(keyhandle, NodeID, byref(pErrorCode) )
            print('Maxon Motor Device Enabled')
    
    #   	ret=CyclicMode(pErrorCode)
    
    #        ret=epos.VCS_SetDisableState(keyhandle, NodeID, byref(pErrorCode) )
    #        print('Maxon Motor Device Disabled')
    
    # 		# Other Option to Read Position
            #ret=GetPositionIs()
    #        ret=epos.VCS_GetVelocityIs(keyhandle, NodeID, byref(pVelocityIs), byref(pErrorCode) )
    #        Omega = pVelocityIs.value
    #        print('Velocity = ' % pVelocityIs)
    
        else:
            print('EPOS4 is in Error State: %#5.8x' % pDeviceErrorCode.value)
            print('EPOS4 Error Description can be found in the EPOS4 Fimware Specification')
    
     
    else:
        print('Could not open Maxon Motor USB-Port')
        print('Keyhandle: %8d' % keyhandle)
        print('Error Openening Port: %#5.8x' % pErrorCode.value)
        
    return keyhandle, NodeID