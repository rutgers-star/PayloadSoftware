#!/usr/bin/env python

"""
A module written to generate commands to control the Blue Canyon Technologies D.C.E. and execute the commands on the device. 
"""

import serial
from Logs.log import log

__author__="Andrew Yu"
__credits__=["Andrew Yu", "Simon Kowerski"]
__creation_date__="2023"

__version__="0.0.0"
__maintainer__="Simon Kowerski"
__email__="sk2790@scarletmail.rutgers.edu"
__status__="Development"


universal = {
    #                            | Address |  Length  |
    "WRITE_HEADER":         [0xEB],
    "READ_HEADER":          [0xED],

    # Address where information is stored
    "WRITE_ADDR":           [0X00,0x00],
    #                       | Address |  Length  |
    "SPEED_ADDR":           [0x04,0x79, 0x00, 0x08], 
    "TORQUE_ADDR":          [0x04,0x89, 0x00, 0x10],

    # Conversion factors for READ information 
    "SPEED_CONV":           [0.2], 
    "TORQUE_CONV":          [0.00000001]
}

def convert_to_hex(wheel_rate,length,conversion_factor=1.0): 
    """
    Converts a wheel_rate into its corresponding hex value

    Args:
        wheel_rate (float): speed OR torque of the wheel
        length (int): the number of hex digits in the output (leading zeros will be added accordingly)
        conversion_factor (float): EU conversion factor as specified on the DCE command table 
    
    Ret:
        str: the resulting hexadecimal expression (exculding the leading 0x)
    """

    nbits=4*length
    wheel_rate=int(wheel_rate/conversion_factor)
    parameter_hex = hex((wheel_rate + (1 << nbits)) % (1 << nbits)) #ensures proper twos compliment is used <-- do we want this...?

    parameter_hex = parameter_hex[2:]

    for i in range(length - len(parameter_hex)):
        parameter_hex='0'+parameter_hex

    #if len(parameter_hex)%2 != 0:
    #    parameter_hex = '0'+parameter_hex

    return parameter_hex

def convert_from_hex(parameter_hex:str,conversion_factor=1.0): 
    """
    Converts a hex value read from the DCE to the corresponding integer value

    Args:
        parameter_hex (str): a hex value formatted like 0xc0ffee which obeys two's complement
        conversion_factor (float): EU conversion factor as specified on the DCE command table 
    
    Ret:
        float: the integer representation of the hex expression +/- one conversion factor from the original
    """

    #hex_arr=parameter_hex.split(" ")

    #ret=0x0
    #for x in hex_arr:
    #    ret=ret<<8
    #    ret+=int(x, 16)

    hex_arr=parameter_hex[2:]
    ret=int(parameter_hex, 16)

    # obey twos compliment
    if len(format(ret,"b"))%4==0:
        ret=ret-(1 << len(format(ret,"b")))

    return ret * conversion_factor

#FIXME: When writing to one wheel, read from DCE to fill in missing values
def set_wheel_torque(wheel_num:int,wheel_rate:float):
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
    command = universal["WRITE_HEADER"].copy()  # add the write header
    command.extend(universal["WRITE_ADDR"])     # add the write address
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
    parameter_hex = convert_to_hex(wheel_rate,8,universal["TORQUE_CONV"][0])
        
    # sets the speed for the correct wheel
    if(wheel_num == 0): # if wheel_num is zero it sets for all 4
        for i in range(1,5):
            # breaks the hex values into groups of two
            wheelSet[0+(4 * (i - 1))] = int(parameter_hex[:2], 16)
            wheelSet[1+(4 * (i - 1))] = int(parameter_hex[2:4], 16)
            wheelSet[2+(4 * (i - 1))] = int(parameter_hex[4:6], 16)
            wheelSet[3+(4 * (i - 1))] = int(parameter_hex[6:], 16)
        
    else: # if a specific wheel num is selected, update that specific wheel
        # breaks the hex values into groups of two
        wheelSet[0+(4 * (wheel_num - 1))] = int("0x"+parameter_hex[:2], 16)
        wheelSet[1+(4 * (wheel_num - 1))] = int("0x"+parameter_hex[2:4], 16)
        wheelSet[2+(4 * (wheel_num - 1))] = int("0x"+parameter_hex[4:6], 16)
        wheelSet[3+(4 * (wheel_num - 1))] = int("0x"+parameter_hex[6:], 16)

    command.extend(wheelSet)

    ret = ""
    for i in range(len(command)):
        command[i] = '0x{:02X}'.format(command[i])
        ret += command[i] + " "

    return ret[:-1], _send_command(ret)

#FIXME: When writing to one wheel, read from DCE to fill in missing values
def set_wheel_speed(wheel_num:int,wheel_rate:float):
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
    log(301)
    command = universal["WRITE_HEADER"].copy()  # add the write header
    command.extend(universal["WRITE_ADDR"])     # add the write address
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
    parameter_hex = convert_to_hex(wheel_rate, 4, universal["SPEED_CONV"][0])

    # sets the speed for the correct wheel
    if(wheel_num == 0): # if wheel_num is zero it sets for all 4
        for i in range(1,5):
            # breaks the hex values into groups of two
            wheelSet[0 + (2 * (i - 1))] = int("0x"+parameter_hex[:2], 16)
            wheelSet[1 + (2 * (i - 1))] = int("0x"+parameter_hex[2:], 16)
        
    else: # if a specific wheel num is selected, update that specific wheel
        # breaks the hex values into groups of two
        wheelSet[0 + (2 * (wheel_num - 1))] = int("0x"+parameter_hex[:2], 16)
        wheelSet[1 + (2 * (wheel_num - 1))] = int("0x"+parameter_hex[2:], 16)
    
    command.extend(wheelSet)

    ret = ""
    for i in range(len(command)):
        command[i] = '0x{:02X}'.format(command[i])
        ret += command[i] + " "

    return ret[:-1], _send_command(ret)

def read_data(read_type:str):
    """
    Generates and sends a code to the DCE to read speed or torque data

    Args:
        read_type (str): Type of data to be read. MUST be either 'SPEED' or 'TORQUE'
    
    Returns:
        int[]: the speed or torque values
        str: the exact data collected from the DCE
        str: The command formatted and ready to send to the DCE
        bool: True if successful, false if an error occured
    """
    log(302)
    command = universal["READ_HEADER"].copy() # add the read header
    
    # Ensures user is requesting either speed or torque data from the DCE
    read_type = read_type.upper()
    if(read_type != "SPEED" and read_type != "TORQUE"):
        log(1302, "- data type not recognized")
        return None, None, None, False

    command.extend(universal[f"{read_type}_ADDR"]) # add the address AND length read
    
    ret_command = ""
    for i in range(len(command)):
        command[i] = '0x{:02X}'.format(command[i])
        ret_command += command[i] + " "
    ret_command=ret_command[:-1]

    send_success=_send_command(ret_command)

    # stop if sending command to the DCE fails, logged in send function
    if not send_success:
        return None, None, ret_command, False

    actual = ''

    # attempt to open serial port
    try:
        serial_port=serial.Serial("/dev/ttyS0", baudrate=9600)

    except Exception:
        log(1304, f"- failed to open serial port /dev/ttyS0 - read - {ret_command}")
        return None, None, ret_command, False

    # attempt to read from serial port
    try:
        actual=serial_port.read((6 + universal[f"{read_type}_ADDR"][3] + 1)*8) # how many bits to be read from the serial port (6 hex values for the header, DATA, 1 hex value for CRC8)

    except Exception:
        log(1304, f"- failed to read from serial port /dev/ttyS0 - {ret_command}")
        return None, None, ret_command, False
    
    log(304, f"- {ret_command}")

    length=universal[f"{read_type}_ADDR"][3]/4

    # Potential spot for error to occur
    # Assumes data collected to be a set of ones and zeros, converts accordingly
    actual=hex(int(actual, 2))[2:]
    dce_header=actual[0:11]
    dce_data=actual[12:-2]
    dce_crc8=actual[-2:]

    wheel_set=["","","",""]
    wheel=0
    data_point=0

    for item in dce_data:
        wheel_set[wheel]+=item
        data_point+=1
        if data_point==length*2:
            wheel_set[wheel]=convert_from_hex(wheel_set[wheel], universal[f"{read_type}_CONV"][0])
            data_point=0
            wheel+=1
    
    if not _verify_output(actual):  
        log(1305)
        return wheel_set, actual, ret_command, False
        
    return wheel_set, actual, ret_command, True

#TODO: Does not have a docstring 
def _verify_output(input_data:str):
    POLYNOMIAL=(0x1070<<3)
    crc=0xFF
    for j in range(0, int((len(input_data)-2)/2)):
        data=crc^int(input_data[(2*j):(2*(j+1))], 16)
        data<<=8
        for i in range(8):
            if((data & 0x8000)!=0):
                data=data^POLYNOMIAL
            data<<=1
        crc=data>>8
        #print(str(input_data[(2*j):(2*(j+1))]) + "\t" + str(hex(crc)[2:]))
    
    return hex(crc)[2:].upper() == input_data[-2:].upper()

def _send_command(hex_code:str):
    """
    Sends a command to the DCE to be executed
    
    Args:
        hex_code (str): A string containing the entire command to be sent to the DCE formatted 0xAB 0xCD 0xEF ....

    Returns
        bool: True if successfully sent, false if an error occurs
    """

    try:
        serial_port = serial.Serial("/dev/ttyS0", baudrate=9600)

    except Exception:
        log(1303, f"- failed to open serial port /dev/ttyS0 - {hex_code}")
        return False

    try:
        serial_port.write(str.encode(hex_code))

    except Exception:
        log(1303, f"- failed to write to serial port /dev/ttyS0 - {hex_code}")
        return False
    
    log(303, f"- {hex_code}")
    return True

#input 1 selects the wheel input 2 sets the torque
#torque is limited to -21.4748 to 21.4748 Nm as specified by BCT documentation
print(set_wheel_torque(2,-21.4748)[0])

#input 1 selects the wheel input 4 sets the speed
#speed is limited to -6553.4 to 6553.4 rpm as specified by BCT documentation
print(set_wheel_speed(4,6334.4781)[0])
print(set_wheel_speed(4,-6355.7)[0])

#Attempts to read data from DCE
#print(read_data("torque"))

#reading tests
length=2
actual=format(0x1acf0000000083de83de7bb87bb800, "b")
actual=hex(int(actual, 2))[2:]
dce_header=actual[0:11]
dce_data=actual[12:-2]
dce_crc8=actual[-2:]

wheel_set=["","","",""]
wheel=0
data_point=0

for item in dce_data:
    wheel_set[wheel]+=item
    data_point+=1
    if data_point==length*2:
        wheel_set[wheel]=convert_from_hex(wheel_set[wheel], .2)
        data_point=0
        wheel+=1
    
print(wheel_set)        
#https://github.com/niccokunzmann/crc8/blob/master/crc8.py
print(_verify_output("1ACF1000000401020304FA"))
