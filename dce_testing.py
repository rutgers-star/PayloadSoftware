#!/usr/bin/env python

"""
A module written to to test custom BCT DCE control code
"""

from Logs.log import log
from dce_control import *
from time import sleep

__author__="Simon Kowerski"
__credits__=["Simon Kowerski"]
__creation_date__="8/8/2024"

log(0)
#set_wheel_speed(1, 0)
set_wheel_torque(1,1)

sleep(10)

vals = read_data("SPEED")
print(bytes.hex(vals))
print(vals)
#print(vals[0])
#print(vals[1])
#hex_code = "0xED 0x04 0x89 0x00 0x10"
#serial_port=serial.Serial("/dev/ttyS0", baudrate=115200)
#packet = bytearray()
#arr = hex_code.split(" ")
#for item in arr:
#    packet.append(int(item, 16))
#serial_port.write(packet)
#print(serial_port.read(16 + 6 + 1))

set_wheel_speed(1, 0)

log(1)


