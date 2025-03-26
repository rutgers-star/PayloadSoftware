#!/usr/bin/env python

"""
A module used to handle the recording of operating logs
00-error-codes.txt contains the event messages that are sent to the .log files
Errors are logged by errors.py with assistance from this module

Atributes:
    __gPath (str): Path to log files
    __quiet (bool): Whether or not to enter quiet mode. When true quiet events aren't logged
"""

import os, time, re
from datetime import date

__author__ = "Simon Kowerski"
__credits__ = ["Simon Kowerski"]
__creation_date__="1/22/2024"

__gPath = "Logs/DailyLogs/"

__quiet = False

__codes__ = {
    #     [String, quiet (True to silence when quiet mode is on)]


    #Experiment Events 0000 - 0099
        0: ["Experiment start", False],
        1: ["Experiment end", False],
        2: ["Known error occurred - experiment safely terminated early", False],
        3: ["Camera not requested - skipping camera startup", False],
        99: ["CRITICAL ERROR - experiment not safely terminated", False],

    #Communication Events 0100 - 0199

    #N/A 0200-0299

    #ADCS Events 0300-0399
        #DCE
        300: ["Requested torque command", True],
        301: ["Requested speed command", True],
        302: ["Requested read command", True],
        303: ["Successfully sent command to DCE", True],
        304: ["Successfully recieved data from DCE", True],
        310: ["Successfully opened DCE serial connection", False],
        311: ["Confirmed DCE Startup", False],

        #IMU
        350: ["Initializing IMU Connection", False],
        351: ["Reading IMU Data", True],
        352: ["IMU Settled", False],
    #Sensor Events 0400-0499
        #Camera
        400: ["Starting Camera", True],
        401: ["Camera Started", False],
        402: ["Closing Camera", True],
        403: ["Camera Closed", False]

    #N/A 0500-0599

    #N/A 0600-0699

    #N/A 0700-0799

    #N/A 0800-0899

    #N/A 0900-0999
}

def log(code:int|str, extra=''):
    """
    Writes an event or error message to the most recent experimnets .log file
        Must open an experiment first using open_experiment()

    Args:
        code (int or string): the event (int) or error (string) being logged
        extra (str): Optional, any additional details to be included in the log
    """
    filename = f"{__gPath}{str(date.today())}.log"
    
    #creates or accesses the days log file
    if not os.path.exists(filename):
        file = open(filename, "w")
    else: 
        file = open(filename, "a")
    
    # writes the correct code to the file
    if type(code) == int:
        if __codes__[code][1] and __quiet:
            return 
        callout="   "
        if code == 0:
            callout = "NEW"
        if code == 1 or code == 2 or code == 99:
            callout = "STP"
       
        if code < 10:
            message = f"{callout} 000{code} - {__codes__[code][0]}"
        elif code < 100:
            message = f"{callout} 00{code} - {__codes__[code][0]}"
        else:   
            message = f"{callout} 0{code} - {__codes__[code][0]}"
    else:
        message = f"ERR {code}"

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    file.write(f'{current_time} {message} {extra}\n')
    file.close()


log(0)
log(310)
log(311)
log(303)
log(1)
