#!/usr/bin/env python

"""
A module used to handle the recording of operating logs
00-error-codes.txt and 01-event-codes.txt contain the messages that are sent to the .log files

Atributes:
    __path (str): Path to log files
"""

import os, time, re
from datetime import date

__author__ = "Simon Kowerski"
__credits__ = ["Simon Kowerski"]
__creation_date__="1/22/2024"

__version__ = "1.0.0"
__maintainer__ = "Simon Kowerski"
__email__ = "kowerski8@gmail.com"
__status__ = "Release"

__path = "Logs/"

def log(code:str, extra=''):
    """
    Writes an event or error message to the most recent experimnets .log file
        Must open an experiment first using open_experiment()

    Args:
        code (int): the error or event being logged
        extra (str): Optional, any additional details to be included in the log
    """
    filename = f"{__path}{str(date.today())}.log"
    
    # accesses the most recent log file
    files=os.listdir(__path)
    logs=[]
    for file in files:
        if re.match("(.*)(\.)(log)", file):
            logs.append(file)
    file = logs[-1:][0]
    file = open(f'{__path}{file}', "a+")
    
    # writes the correct code to the file
    if code < 1000:
        codemsg = open(f"{__path}01-event-codes.txt", "r")
        message = f"    {codemsg.readlines()[code]}"
    else:
        codemsg = open(f"{__path}00-error-codes.txt", "r")
        message = f"ERR {codemsg.readlines()[code-1000]}"

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    file.write(f'{current_time} {message} {extra}'[:-1])
    file.close()

def open_experiment(experiment_num:int):
    """
    Creates a log file for the most recent experiment. All logs will be written to the most recent log file.
    Log files will be named YYYY-MM-DD_Exp-#.log where the # is a count of the number of experiments run that day
        For example:
        -The first experiment run on 4/12/2024 will be called 2024-4-12_Exp-1.log 
        -The fourth experiment run on 4/12/2024 will be called 2024-4-12_Exp-4.log 
    
    Args:
        experiment_num (int): the number of the experimnet being run as pulled from the experiment table 
    """

    current_time = time.strftime("%H:%M:%S", time.localtime())
    current_date = str(date.today())

    files=os.listdir(__path)
    logs=[]
    for file in files:
        if re.match(f"{current_date}_Exp-[0-9]+\.log", file):
            logs.append(file)

    filename = f"{__path}{current_date}_Exp-{len(logs)+1}.log"
    file = open(filename, "w")

    file.close()
    file = open(filename, "a")

    file.write(f'Experiment {experiment_num}\n')
    file.write(f'{current_date}\n')
    file.write(f'{current_time}\n')
    file.write(f'{len(logs)} other experiment(s) run today\n\n')
    file.close()

