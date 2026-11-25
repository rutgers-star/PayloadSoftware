import numpy as np
import time
from sensor_control import sensor_start, sensor_read, sensor_stop
from camera_control import init_camera, close_camera

k = 1
maxiter = 100
force = np.zeros((maxiter,3))
torque = np.zeros((maxiter,3))
status = np.zeros((maxiter,3))

init_camera()
bota_ft_sensor_driver = sensor_start("bota_binary_gen0.json")

startTime = time.time_ns() / 1_000_000
currentTime = time.time_ns() / 1_000_000
iterations_before_60 = 0
maxDelta = -1
while k < maxiter:
    [s,force[k,:],torque[k,:]] = sensor_read(bota_ft_sensor_driver)
    currentTime = time.time_ns() / 1_000_000
    delta = currentTime - currentTime
    if currentTime - startTime < 60000: 
        iterations_before_60 += 1
    maxDelta = max(delta, maxDelta)
    print(f"iter: {k}\nForce: {force[k]}\n Torque: {torque[k]}\n")
    k += 1
    currentTime = time.time_ns() / 1_000_000

print(f"Max delta: {maxDelta}, Iterations before 60s: {iterations_before_60}")
sensor_stop(bota_ft_sensor_driver)
close_camera()