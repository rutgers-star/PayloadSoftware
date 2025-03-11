# PayloadSoftware
This package contains the core code responsible for managing all components of the flight software related to Payload. This includes the Blue Canyon Technologies Drive Control Electronics (DCE), Inertial Measurement Unit Senors (IMU), and the camera systems. It also includes code for performing experiments with these components and presenting data generated. Additional information about flight hardware can be found in the [Mission Design Document](https://drive.google.com/file/d/1k6YuuXuI0GU9KWWqZzIuja9gc7hxLAv-/view).

## camera_control.py
A module that accesses the camera, can be imported using the command:

```python
from camera_control import init_camera, close_camera
```
Failure to start up camera will result in shut down of the current running experiement. This will log error `1400` with the timestamp of this termination. See `error.py` in the log package for more information.

Sucessful startup or shutdown of camera will log events 
`400-404`. See `log.py` in the log package for more information.

## control.py FIXY FIX
A module which contains the definitions for control algroithms to drive a motor for the 1.D. tests of the SPICEsat testbench. Can be imported using the command:
```python
from control import PID_control
```
PID_control requires tweleve parameters listed down below, inorder to perform its calculations and returns an array of those results. `theta_d` is the desired angle of rotation, `dt` is the time difference, `I` and `J` are the moment of inertia for the wheels, the rest of the values needed are numpy declarations of `MAX_ITER`.

```python
def PID_control(theta_d, k, t, dt, I, J, theta, vel, acc, err, errdot, ecumul)
```

## dce_control.py
A module that contains all the necessary code to operate the Blue Canyon Technologies DCE. Can be imported using the command:
```python
from dce_control import set_wheel_torque, set_wheel_speed, startup, read_data
```
### startup
Establishes a serial connection to the `HR_RUN_COUNT` register, and verifies that the DCE has sucessfully ran. 
If unable to connect sucessfully to serial port, throws `ERROR 1310`, otherwise event `310` will be logged.  

Failure when reading from `HR_RUN_COUNT` or incorrect values will result in `ERROR 1311`, otherwise `log 311`. Check `Logging Events` and `Logging Errors` under the log package for more information.

### set_wheel_torque & set_wheel_speed
Accepts two parameters, `wheel_num`: an int value between 0 and 4 where 0 selects all four wheel, and 1-4 selected individual wheel, and `wheel_rate`: a float value that holds the wheel's torque (in N/m) or speed (in RPM) accordingly. A string of hex values will be returned which indicate the command that was sent to the DCE. 
```python
def set_wheel_torque(wheel_num:int, wheel_rate:float)
def set_wheel_speed(wheel_num:int, wheel_rate:float)
```
These will use `convert_to_hex` to convert the given integer values to hex values formatted for the DCE.
```python
def convert_to_hex(wheel_rate,length, conversion_factor=1.0)
```
`send_command_` will take the result of `convert_to_hex` and send the converted hex values to the DCE.
```python
def _send_command(hex_code:str)
```
Successful excution of _______ will `log 300` and `log 301` otherwise will throw `ERROR 1300` and `ERROR 1301`.
### read_data WHAT DOES THIS RETURN
Accepts a string value of either `SPEED` or `TORQUE` in order to generate and send a code to the DCE to allow for reading of torque or speed and `log 302`. Failure to sucessful connect to port or incorrect input will raise `ERROR 1302`.
```python
def read_data(read_type:str)
```
Failure to read from port will raise `ERROR 1304` and `ERROR 1305` is incorrect input if given. Will use `veryify_output` to check, return true if correct else false.
```python
def verify_output(input_data:str)
```
A sucessfully read from the DCE will `log 304`.

## imu_control.py
A module that accesses the IMU for one-dimensional test, can be imported using the command:
```python
from imu_control import init_imu, imu_data
```
Initializes the IMU using serial and `log 350`. Failure to open port connection or settle will throw `ERROR 1350`, otherwise will `log 1352`. 

### imu_data FINISH
Collects data from a connected IMU Unit, `log 351`
```python
def imu_data(imu, yaw0, yawOld)
```

## main_loop.py SIMON FIXY
This module contains all the necessary compoments to run a one-dimensional test bench of the S.T.A.R SPICEsat.

Includes the following classes:
```python
import math
import time
import subprocess
from ctypes import *
import numpy as np 
import matplotlib.pyplot as plt

from imu_control import init_imu, imu_data
from camera_control import init_camera, close_camera
from control import PID_control
from plot_tools import plot_sloshy
from dce_control import set_wheel_torque, set_wheel_speed, startup

from Logs.log import log
from Logs.errors import ERROR
```

This module will:  
* Calculate all Initial Values
* Startup Pressure Sensors
* Startup Motor
* Startup IMU
* Startup Camera
* Run the Control Test
* End the Experiment -> Shuts down all running equipment

## plot_tools.py
A module which uses MatPlotLib to generate plots of collected the data for 1-Dimensional tests, can be imported with:
```python
from plot_tools import plot_sloshy
```
### plot_sloshy
Using MatPlotLib:
```python
import matplotlib.pyplot as plt
```
Graphs the motion of sloshing using the IMU and PID controller for further analysis.


All guideline for logging will be found in the [Payload Software Standards](https://docs.google.com/document/d/1vicnkUB_dqbaCpopz8N8pzhCTJqari4AZ5WBYJJv5HY/edit#heading=h.yexhmihjoetb).