import numpy as np
from sensor_control import sensor_start, sensor_read, sensor_stop

k = 1
maxiter = 100
force = np.zeros((maxiter,3))
torque = np.zeros((maxiter,3))
status = np.zeros((maxiter,3))

bota_ft_sensor_driver = sensor_start("bota_binary_gen0.json")

while k < maxiter:
    [s,force[k,:],torque[k,:]] = sensor_read(bota_ft_sensor_driver)
    print(f"iter: {k}\nForce: {force[k]}\n Torque: {torque[k]}\n")
    k += 1

sensor_stop(bota_ft_sensor_driver)