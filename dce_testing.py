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

set_wheel_torque(1, 1)

sleep(3)

vals = read_data("TORQUE")

print(vals[0])
print(vals[1])

set_wheel_torque(0)

log(1)


