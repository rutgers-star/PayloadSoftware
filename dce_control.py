#!/usr/bin/env python

"""
A module written to generate commands to control the Blue Canyon Technologies D.C.E. and execute the commands on the device. 

Atributes:
    universal - an array to store commonly used values such as DCE memory addresses
    serial_port - an object which stores an opened connection to the serial port
"""

import serial
from Logs.log import log
from Logs.errors import ERROR
from time import sleep
from decimal import *

__author__="Andrew Yu"
__credits__=["Andrew Yu", "Simon Kowerski"]
__creation_date__="2023"

serial_port=None

universal={
    #                            | Address |  Length  |
    "WRITE_HEADER":         [0xEB],
    "READ_HEADER":          [0xED],

    # Address where information is stored
    "WRITE_ADDR":           [0X00,0x00],
    #TODO: Make these speed measure not speed command
    #                       | Address |  Length  |
    "SPEED_ADDR":           [0x04,0x69, 0x00, 0x10], 
    "TORQUE_ADDR":          [0x04,0x89, 0x00, 0x10],

    # Conversion factors for WRITE information 
    "SPEED_WRITE_CONV":           [0.2], 
    "TORQUE_WRITE_CONV":          [1e-8],

    # Conversion factors for READ information 
    "SPEED_READ_CONV":           [0.002], 
    "TORQUE_READ_CONV":          [1e-8]
}

def startup():
    """
    Opens the serial connection and reads from the HR_RUN_COUNT register to ensure that the DCE is running
    """

    if(serial_port):
        return

    # opens serial Connection
    try:
        serial_port=serial.Serial("/dev/ttyS0", 115200, timeout=1)
    except Exception:
        raise ERROR(1310)
    
    sleep(.2)

    #TODO: Finish This
    # attempts to read from HR_RUN_COUNT
    try:
        _send_command("0xec 0x04 0xfe 0x00 0x04")
        val = serial_port.read(4)
           
    except Exception:
        raise ERROR(1311)
    
    log(310)

#FIXME Probably needs more percision for the torque things
def convert_to_hex(wheel_rate,length, conversion_factor=1.0): 
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

    return parameter_hex

#FIXME Probably needs more percision for the torque things
def convert_from_hex(parameter_hex:str, conversion_factor=1.0): 
    """
    Converts a hex value read from the DCE to the corresponding integer value

    Args:
        parameter_hex (str): a hex value formatted like 0xc0ffee OR c0ffee which obeys two's complement
        conversion_factor (float): EU conversion factor as specified on the DCE command table 
    
    Ret:
        float: the integer representation of the hex expression +/- one conversion factor from the original
    """

    ret=int(parameter_hex, 16)
    twos=int(parameter_hex[0], 16)

    # obey twos compliment
    if len(format(twos,"b"))%4==0:
        print("here")
        ret=ret-(1 << len(format(ret,"b")))

    return ret * conversion_factor

#FIXME: When writing to one wheel, read from DCE to fill in missing values
#FIXME: REPLACE SATURATION VALUES
def set_wheel_torque(wheel_num:int, wheel_rate:float):
    """
    Generates and sends a code to the DCE to set the torque on one or all of the reaction wheels.
        Accepts a wheel number between 0 and 4 (inclusive), where 0 selects all 4 wheels
        Accepts a torque between -21.4748 and +21.4748 (Nm) (exclusive)

    Args:
        wheel_num (int): The wheel to be selected 
        wheel_rate (float): The torque to be applied to the wheel
    
    Returns:
        str: The command formatted and ready to send to the DCE
    """
    log(300)
    command = universal["WRITE_HEADER"].copy()  # add the write header
    command.extend(universal["WRITE_ADDR"])     # add the write address
    command.extend([0x00, 0x13])                # add the length of the command - 19 bytes 
    command.extend([0x07,0x0D, wheel_num])      # call the 'SetWheelTorque32' command
    
    # Ensures requested rate is within safe operating bounds
    if wheel_rate>21.4748 or wheel_rate<-21.4748:
        raise ERROR(1300, f"requested wheel torque is out of operational limits - {wheel_rate}")
    
    # Ensures wheel selected properly
    if(wheel_num > 4 or wheel_num < 0):
        raise ERROR(1300, f"wheel selected improperly - {wheel_num}")
    
    #          |      Wheel 1      |      Wheel 2      |      Wheel 3      |      Wheel 4      |
    wheelSet = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    
    # preforms the EU conversion and and formats it into hex
    parameter_hex = convert_to_hex(wheel_rate,8,universal["TORQUE_WRITE_CONV"][0])
        
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

    ret=ret[:-1]
    _send_command(ret)
    return ret

#FIXME: When writing to one wheel, read from DCE to fill in missing values
#FIXME: REPLACE SATURATION VALUES
def set_wheel_speed(wheel_num:int, wheel_rate:float):
    """
    Generates and sends a code to the DCE to set the speed of one or all of the reaction wheels.
        Accepts a wheel number between 0 and 4 (inclusive), where 0 selects all 4 wheels
        Accepts a speed in RPM between -6553.4 and +6553.4 (RPM) (exclusive)

    Args:
        wheel_num (int): The wheel to be selected 
        wheel_rate (float): The speed to set each wheel to
    
    Returns:
        str: The command formatted and ready to send to the DCE
    """
    log(301)
    command = universal["WRITE_HEADER"].copy()  # add the write header
    command.extend(universal["WRITE_ADDR"])     # add the write address
    command.extend([0x00, 0x0B])                # add the length of the command - 11 byets?
    command.extend([0x07,0x0A, wheel_num])      # call the 'SetWheelSpeed4' command

    # Ensures requested rate is within safe operating bounds
    if wheel_rate>6553.4 or wheel_rate<-6553.4:
        raise ERROR(1301, f"requested wheel rate is out of operational limits - {wheel_rate}")
    
    # Ensures wheel is requested properly
    if(wheel_num > 4 or wheel_num < 0):
        raise ERROR(1301, f"wheel selected incorrectly - {wheel_num}")
    
    #          | Wheel 1 | Wheel 2 | Wheel 3 | Wheel 4 |
    wheelSet = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    
    # preforms the EU conversion and and formats the rate into hex
    parameter_hex = convert_to_hex(wheel_rate, 4, universal["SPEED_WRITE_CONV"][0])

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

    ret=ret[:-1]
    _send_command(ret)
    return ret

def read_data(read_type:str):
    """
    Generates and sends a code to the DCE to read speed or torque data

    Args:
        read_type (str): Type of data to be read. MUST be either 'SPEED' or 'TORQUE'
    
    Returns:
        int[]: the speed or torque values collected
        str: the exact data collected from the DCE
        str: The command formatted and ready to send to the DCE
    """
    log(302)
    command = universal["READ_HEADER"].copy() # add the read header
    
    # Ensures user is requesting either speed or torque data from the DCE
    read_type = read_type.upper()
    if(read_type != "SPEED" and read_type != "TORQUE"):
        raise ERROR(1302, "data type not recognized")

    command.extend(universal[f"{read_type}_ADDR"]) # add the address AND length read
    
    ret_command = ""
    for i in range(len(command)):
        command[i] = '0x{:02X}'.format(command[i])
        ret_command += command[i] + " "
    ret_command=ret_command[:-1]

    _send_command(ret_command)        

    actual=0

    # attempt to read from serial port
    read_length=6+16+1
    try:
        actual=serial_port.read(read_length) # how many bytes to be read from the serial port (6 hex values for the header, DATA, 1 hex value for CRC8)

    except Exception:
        raise ERROR(1304, f"failed to read from serial port - {ret_command}")
    
    # verify the correct output is recieved
    if(len(actual) != read_length):
        raise ERROR(1305, f"did not recieve the correct number of bytes - Requested: {read_length} - Recieved: {len(actual)} - {ret_command}")

    actual=bytes.hex(actual)

    if(not _verify_output(f'0x{actual}')):
        raise ERROR(1305)

    # TODO:
    # perform conversions on actual
    wheel_arr = [actual[12:20], actual[20:28], actual[28:36], actual[36:44]]
    for i in len(wheel_arr):
        wheel_arr[i] = convert_from_hex(wheel_arr[i], universal[f"{read_type}_READ_CONV"][0])
    
    log(304, f"- Output: {actual}")

    return wheel_arr, actual, ret_command

def _verify_output(input_data:str):
    """
    Determines whether or not the optupt string generated by the DCE was correct

    Args:
        input_data (str): the data read from the DCE, not seperated by spaces, including the leading '0x'
    
    Returns:
        bool: True if the output matches, false if not
    """
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
    
    return hex(crc)[2:].upper() == input_data[-2:].upper()

def _send_command(hex_code:str):
    """
    Sends a command to the DCE to be executed
    
    Args:
        hex_code (str): A string containing the entire command to be sent to the DCE formatted 0xAB 0xCD 0xEF ....
    """

    # ensure serial connection is open
    if(not serial_port):
        raise ERROR(1303, f"serial port not open")

    # make packet to send hex values to serial port
    packet = bytearray()
    arr = hex_code.split(" ")
    for item in arr:
        packet.append(int(item, 16))

    # write packet to the serial port
    try:
        serial_port.write(packet)

    except Exception:
        raise ERROR(1303, f"failed to write to serial port at /dev/ttyS0 - {hex_code}")
    
    log(303, f"- {hex_code}")

#read_data('SPEED')
#set_wheel_speed(1,1)
#val=convert_from_hex("0x002161d4", universal["SPEED_CONV"])
#print(val)
'''
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
print(_verify_output("1ACF1000000401020304FA"))
'''