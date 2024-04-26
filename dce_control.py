#!/usr/bin/env python

"""
A module written to generate commands to control the Blue Canyon Technologies D.C.E. and execute the commands on the device. 
**MODULE STILL BEING DEVELOPED**
"""

from Logs.log import log

__author__="Andrew Yu"
__credits__=["Andrew Yu", "Simon Kowerski"]
__creation_date__="2023"

__version__="0.0.0"
__maintainer__="Simon Kowerski"
__email__="sk2790@scarletmail.rutgers.edu"
__status__="Development"


addresses = {
    #                            | Address |
    "WRITE_HEADER":         [0xEB,0x00,0x00],

    # Address where speed information is stored
    "SPEED_ADDR":           [0x04,0x79], 
    "TORQUE_ADDR":          [0x04,0x89]
}


def convert_hex(wheel_rate, nbits): 
    """
    Converts a wheel_rate into its corresponding hex value

    Args:
        wheel_rate (float): speed OR torque of the wheel
        nbits (int): number of 
    
    Ret:
        str: the resulting hexadecimal expression
    """
    parameterHex = hex((int(wheel_rate) + (1 << nbits)) % (1 << nbits)) #find out what this does 

    if len(parameterHex) <= 4:
        if len(parameterHex) <=3:
            parameterHex = '0'+parameterHex[2:]
            return(parameterHex)
        else:
            parameterHex = parameterHex[2:]
            return(parameterHex)

    else:
        parameterHex = parameterHex[2:]

        if len(parameterHex)%2 != 0:
            parameterHex = '0'+parameterHex

        return(parameterHex)

def set_wheel_torque(wheel_num:int,wheel_rate:int):
    """
    Generates and sends a code to the DCE to set the torque on one or all of the reaction wheels.
        Accepts a wheel number between 0 and 4 (inclusive), where 0 selects all 4 wheels
        Accepts a torque between -21.4748 and +21.4748 (exclusive)

    Args:
        wheel_num (int): The wheel to be selected 
        wheel_rate (float): The torque to be applied to the wheel
    
    Returns:
        str: The command formatted and ready to send to the DCE
        bool: True if successful, false if an error occured
    """
    log(300)
    command = addresses["WRITE_HEADER"].copy()  # add the write header
    command.extend([0x00, 0x13])                # add the length of the command - 19 bytes 
    command.extend([0x07,0x0D, wheel_num])      # call the 'SetWheelTorque32' command
    
    # Ensures requested rate is within safe operating bounds
    if wheel_rate>21.4748 or wheel_rate<-21.4748:
        log(1300, "- requested wheel torque is out of operational limits")
        return None, False
    
    # Ensures wheel selected properly
    if(wheel_num > 4 or wheel_num < 0):
        log(1300, "- wheel selected improperly")
        return None, False
    
    #          |      Wheel 1      |      Wheel 2      |      Wheel 3      |      Wheel 4      |
    wheelSet = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    
    # preforms the EU conversion and and formats it into hex
    parameterHex = convert_hex(int(wheel_rate/0.00000001),32)
        
    # sets the speed for the correct wheel
    if(wheel_num == 0): # if wheel_num is zero it sets for all 4
        for i in range(1,5):
            # breaks the hex values into groups of two
            wheelSet[0+(4 * (i - 1))] = int(parameterHex[:2], 16)
            wheelSet[1+(4 * (i - 1))] = int(parameterHex[2:4], 16)
            wheelSet[2+(4 * (i - 1))] = int(parameterHex[4:6], 16)
            wheelSet[3+(4 * (i - 1))] = int(parameterHex[6:], 16)
        
    else: # if a specific wheel num is selected, update that specific wheel
        # breaks the hex values into groups of two
        wheelSet[0+(4 * (wheel_num - 1))] = int("0x"+parameterHex[:2], 16)
        wheelSet[1+(4 * (wheel_num - 1))] = int("0x"+parameterHex[2:4], 16)
        wheelSet[2+(4 * (wheel_num - 1))] = int("0x"+parameterHex[4:6], 16)
        wheelSet[3+(4 * (wheel_num - 1))] = int("0x"+parameterHex[6:], 16)

    command.extend(wheelSet)

    ret = ""
    for i in range(len(command)):
        command[i] = hex(command[i])
        ret += command[i] + " "

    log(301)

    return ret[:-1], _send_command(ret)

def set_wheel_speed(wheel_num:int,wheel_rate:int):
    """
    Generates and sends a code to the DCE to set the speed of one or all of the reaction wheels.
        Accepts a wheel number between 0 and 4 (inclusive), where 0 selects all 4 wheels
        Accepts a torque between -6553.4 and +6553.4 (exclusive)

    Args:
        wheel_num (int): The wheel to be selected 
        wheel_rate (float): The speed to set each wheel to
    
    Returns:
        str: The command formatted and ready to send to the DCE
        bool: True if successful, false if an error occured
    """
    log(302)
    command = addresses["WRITE_HEADER"].copy()  # add the write header
    command.extend([0x00, 0x0B])                # add the length of the command - 11 byets?
    command.extend([0x07,0x0A, wheel_num])      # call the 'SetWheelSpeed4' command

    # Ensures requested rate is within safe operating bounds
    if wheel_rate>6553.4 or wheel_rate<-6553.4:
        log(1301, "- requested wheel rate is out of operational limits")
        return None, False
    
    # Ensures wheel is requested properly
    if(wheel_num > 4 or wheel_num < 0):
        log(1301, "- wheel selected incorrectly")
        return None, False
    
    #          | Wheel 1 | Wheel 2 | Wheel 3 | Wheel 4 |
    wheelSet = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    
    # preforms the EU conversion and and formats the rate into hex
    parameterHex = convert_hex(wheel_rate/0.2, 16)

    # sets the speed for the correct wheel
    if(wheel_num == 0): # if wheel_num is zero it sets for all 4
        for i in range(1,5):
            # breaks the hex values into groups of two
            wheelSet[0 + (2 * (i - 1))] = int("0x"+parameterHex[:2], 16)
            wheelSet[1 + (2 * (i - 1))] = int("0x"+parameterHex[2:], 16)
        
    else: # if a specific wheel num is selected, update that specific wheel
        # breaks the hex values into groups of two
        wheelSet[0 + (2 * (wheel_num - 1))] = int("0x"+parameterHex[:2], 16)
        wheelSet[1 + (2 * (wheel_num - 1))] = int("0x"+parameterHex[2:], 16)
    
    command.extend(wheelSet)

    ret = ""
    for i in range(len(command)):
        command[i] = hex(command[i])
        ret += command[i] + " "

    log(303)

    return ret[:-1], _send_command(ret)

def read_data(readType):
    #read command indictor byte
    command = [0xEC]
    if "s" in readType or "S" in readType:
        #get speed address and set the read length to 8 as there is two bytes for each of the four wheels
        command.extend(addresses["SPEED_ADDR"])
        command.extend([0x00,0x08])

    elif "t" in readType or "T" in readType:
        #get torque address and set the read length to 16 as there is four bytes for each of the four wheels
        command.extend(addresses["TORQUE_ADDR"])
        command.extend([0x00,0x10])

    else:
        print("Selected Address read has not been added or is incorrect\nExiting . . .")
        exit()

    #print final command
    #will eventually become a pySerial Function to talk to the DCE
    for i in range(len(command)):
        print(hex(command[i]),end=' ')

def _send_command(hex_code):
    """
    Sends a command to the DCE to be executed
    
    Args:
        hex_code (str): A string containing the entire command to be sent to the DCE

    Returns
        bool: True if successfully sent, false if an error occurs
    """
    
    log(1303, f"- {hex_code}")
    return False

#input 1 selects the wheel input 2 sets the torque
#torque is limited to -21.4748 to 21.4748 Nm as specified by BCT documentation
print(set_wheel_torque(2,15)[0])

#input 1 selects the wheel input 4 sets the speed
#speed is limited to -6553.4 to 6553.4 rpm as specified by BCT documentation
print(set_wheel_speed(4,1500)[0])
