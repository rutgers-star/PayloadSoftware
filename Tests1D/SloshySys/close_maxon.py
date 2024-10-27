# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 10:57:47 2023

@author: mfogel
"""


from ctypes import *

# function definition
def close_maxon(keyhandle,NodeID, epos):

    pErrorCode=c_uint()    
    ret=epos.VCS_SetDisableState(keyhandle, NodeID, byref(pErrorCode) )
    print('Maxon Motor Device Disabled')
    
    # Close Com-Port
    ret=epos.VCS_CloseDevice(keyhandle, byref(pErrorCode) )
#    print('Error Code Closing Port: %#5.8x' % pErrorCode.value)    
    
    return
