
import serial
import serial.tools.list_ports
import math
import time
import numpy as np 
from matplotlib import pyplot as plt

ports=serial.tools.list_ports.comports()
#print(ports[0])
#print(ports[0].device)
#for p in ports:
#    print(p.device)
#print(len(ports), 'ports found')



#baud=115200
#imu = serial.Serial('/dev/ttyUSB1',baud, timeout = 5)

baud=115200
imu = serial.Serial(ports[0].device,baud, timeout = 5)
    