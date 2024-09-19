#!/usr/bin/env python

"""
A module used to handle the recording of operating logs
00-error-codes.txt and 01-event-codes.txt contain the messages that are sent to the .log files

Atributes:
    __gPath (str): Path to log files
"""

import os, time, re
from datetime import date

__author__ = "Simon Kowerski"
__credits__ = ["Simon Kowerski"]
__creation_date__="1/22/2024"

__gPath = "Logs/"

def log(code:str, extra=''):
    """
    Writes an event or error message to the most recent experimnets .log file
        Must open an experiment first using open_experiment()

    Args:
        code (int): the error or event being logged
        extra (str): Optional, any additional details to be included in the log
    """
    filename = f"{__gPath}{str(date.today())}.log"
    
    # accesses the most recent log file
    files=os.listdir(__gPath)
    logs=[]
    for file in files:
        if re.match("(.*)(\.)(log)", file):
            logs.append(file)
    file = logs[-1:][0]
    file = open(f'{__gPath}{file}', "a+")
    
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

    files=os.listdir(__gPath)
    logs=[]
    for file in files:
        if re.match(f"{current_date}_Exp-[0-9]+\.log", file):
            logs.append(file)

    filename = f"{__gPath}{current_date}_Exp-{len(logs)+1}.log"
    file = open(filename, "w")

    file.close()
    file = open(filename, "a")

    file.write(f'Experiment {experiment_num}\n')
    file.write(f'{current_date}\n')
    file.write(f'{current_time}\n')
    file.write(f'{len(logs)} other experiment(s) run today\n\n')
    file.close()

