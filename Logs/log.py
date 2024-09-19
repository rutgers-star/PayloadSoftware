#!/usr/bin/env python

"""
A module used to handle the recording of operating logs
00-error-codes.txt contains the event messages that are sent to the .log files
Errors are logged by errors.py with assistance from this module

Atributes:
    __gPath (str): Path to log files
"""

import os, time, re
from datetime import date

__author__ = "Simon Kowerski"
__credits__ = ["Simon Kowerski"]
__creation_date__="1/22/2024"

__gPath = "Logs/Daily Logs/"

def log(code:int|str, extra=''):
    """
    Writes an event or error message to the most recent experimnets .log file
        Must open an experiment first using open_experiment()

    Args:
        code (int or string): the error or event being logged
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
        codemsg = open(f"{__gPath}00-event-codes.txt", "r")
        message = f"    {codemsg.readlines()[code]}"[:-1]
    else:
        message = f"ERR {code}"

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    file.write(f'{current_time} {message} {extra}\n')
    file.close()
