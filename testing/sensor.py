
import os
import bota_driver
import numpy as np

def sensor_start(config_name: str):
    # Bota Serial Binary Gen0
    cwd = os.getcwd()
    config_path = os.path.join(cwd, config_name)
    print(config_path)


    try:
    # Create driver instance
        bota_ft_sensor_driver = bota_driver.BotaDriver(config_path)
#        print( bota_ft_sensor_driver)
    
    # Transition driver from UNCONFIGURED to INACTIVE state
        if not bota_ft_sensor_driver.configure():
            raise RuntimeError("Failed to configure driver")

    # Uncomment to tare the sensor
        if not bota_ft_sensor_driver.tare():
            raise RuntimeError("Failed to tare sensor")

    # Transition driver from INACTIVE to ACTIVE state
        if not bota_ft_sensor_driver.activate():
            raise RuntimeError("Failed to activate driver")

    except:    
       print("Bota sensor failed to start")
       return None
  
#    print("EXITING sensor_start")
    
    return bota_ft_sensor_driver

    

def sensor_read(bota_ft_sensor_driver):
    ########################
    ## CONTROL LOOP START ##
    ########################

    # Define the example duration
#    EXAMPLE_DURATION = 10.0  # seconds

    # Define the reading frequency
#    READING_FREQUENCY = 10.0  # Hz

#    start_time = time.perf_counter()  # High-resolution start time
#    next_execution_time = start_time

#    while time.perf_counter() - start_time < EXAMPLE_DURATION and not stop_flag:
        # Read frame
    bota_frame = bota_ft_sensor_driver.read_frame()

        # Extract the data from the bota_frame
    status = bota_frame.status
    force = bota_frame.force  
    torque = bota_frame.torque
#    timestamp = bota_frame.timestamp
#    temperature = bota_frame.temperature
#    acceleration = bota_frame.acceleration
#    angular_rate = bota_frame.angular_rate

    #################################
    ## YOUR CONTROL LOOP CODE HERE ##
    #################################
#    print(force,"  ", torque)

    # Wait until next execution time
#    next_execution_time += 1.0/READING_FREQUENCY
#    sleep_time = max(0, next_execution_time - time.perf_counter())
#    time.sleep(sleep_time)

    # Transition driver from ACTIVE to INACTIVE state
#    if not bota_ft_sensor_driver.deactivate():
#        raise RuntimeError("Failed to deactivate driver")
    
    # Shutdown the driver
#    if not bota_ft_sensor_driver.shutdown():
#        raise RuntimeError("Failed to shutdown driver")

#    print("SENSOR READ - Completition WITHOUT errors.")
    
    return [status, force, torque]

def sensor_stop(bota_ft_sensor_driver):
    # Transition driver from ACTIVE to INACTIVE state
    if not bota_ft_sensor_driver.deactivate():
        raise RuntimeError("Failed to deactivate driver")
    
    # Shutdown the driver
    if not bota_ft_sensor_driver.shutdown():
        raise RuntimeError("Failed to shutdown driver")


k = 1
maxiter = 100
force = np.zeros((maxiter,3))
torque = np.zeros((maxiter,3))
status = np.zeros((maxiter,3))

bota_ft_sensor_driver = sensor_start("bota_binary_gen0.json")

while k < maxiter:
    [s,force[k,:],torque[k,:]] = sensor_read(bota_ft_sensor_driver)
    k += 1

sensor_stop(bota_ft_sensor_driver)