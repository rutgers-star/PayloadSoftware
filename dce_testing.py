from Logs.log import log, open_experiment
from dce_control import *
from time import sleep

open_experiment(0)

again=True

def error_handler():
    #set_wheel_speed(0, 0)
    #set_wheel_torque(0, 0)
    print("ERROR")
    print("An error occured, see log file for details")
    #print("Wheel speed and torque set to zero as a precaution")
    print("Ending experiment")

while again:
    setting=input("Do you want to test SPEED or TORQUE: ")
    setting=setting.upper()
    while not (setting=="TORQUE" or setting=="SPEED"):
        print("Invalid input")
        setting=input("Do you want to test SPEED or TORQUE: ")

    value=input(f'Enter the desired {setting.lower()} value: ')
    
    match setting:
        case "TORQUE":
            result=set_wheel_torque(1, int(value))
        case "SPEED":
            result=set_wheel_speed(1, int(value))
        
    if not result[-1]:
        error_handler()
        again=False

    else:
        sleep(15)

        print(read_data(setting)[0])

        sleep(5)
        
        print("Resetting wheels")

        set_wheel_speed(0, 0)
        set_wheel_torque(0, 0)

        sleep(15)

        if input("Do you wish to test another value (Y or N)?") != "Y": 
            again=False




#do you want to read speed or torque (s or t)
#what value do you want to set it to?
#set the speed
#success or failure
#wait 15 seconds
#read from dce
#success or failure
#output result
#enter another?