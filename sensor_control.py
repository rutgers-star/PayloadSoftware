"""
A module to control the torque sensor 
"""

from Logs.log import log
from Logs.errors import ERROR
import os
import bota_driver

author="Shreyas Bhatkande"
credits=["Shreyas Bhatkande"]
creation_date="2/22/2025"

def sensor_start(config_name: str):
    """
    Activate the torque sensor
    
    Raises:
        ERROR(1410) - Torque sensor: Failed to configure driver
        ERROR(1411) - Torque sensor: Failed to tare sensor
        ERROR(1412) - Torque sensor: Failed to activate driver
        ERROR(1414) - Failed to start torque sensor

    Returns:
        BotaDriver: The bota sensor driver object
    """
    log(410)
    # Bota Serial Binary Gen0
    cwd = os.getcwd()
    config_path = os.path.join(cwd, config_name)

    try:
        # Create driver instance
        bota_ft_sensor_driver = bota_driver.BotaDriver(config_path)
    
        # Transition driver from UNCONFIGURED to INACTIVE state
        if not bota_ft_sensor_driver.configure():
            raise ERROR(1410)
        if not bota_ft_sensor_driver.tare():
            raise ERROR(1411) 
        # Transition driver from INACTIVE to ACTIVE state
        if not bota_ft_sensor_driver.activate():
            raise ERROR(1412) 

    except:    
        raise ERROR(1413)
  
    return bota_ft_sensor_driver

def sensor_read(bota_ft_sensor_driver):
    """
    Reads force torque and status from torque sensor
    
    Raises:
        ERROR(1414) - Failed to read from torque sensor

    Returns:
        int - The current iteration
        float[3] - The force vector
        float[3] - The torque vector
    """
    log(412)
    try:
        bota_frame = bota_ft_sensor_driver.read_frame()

        # Extract the data from the bota_frame
        status = bota_frame.status
        force = bota_frame.force  
        torque = bota_frame.torque
    except Exception:
        raise ERROR(1414)

    return [status, force, torque]

def sensor_stop(bota_ft_sensor_driver):
    """
    Deactivates and shuts down the torque sensor
    
    Raises:
        ERROR(1415) - Torque sensor: Failed to deactivate driver
        ERROR(1416) - Torque sensor: Failed to shutdown driver
        ERROR(1417) - Torque sensor failed to stop
    """
    log(413)
    
    try:
        # Transition driver from ACTIVE to INACTIVE state
        if not bota_ft_sensor_driver.deactivate():
            raise ERROR(1415)
        
        # Shutdown the driver
        if not bota_ft_sensor_driver.shutdown():
            raise ERROR(1416)
    except Exception:
        raise ERROR(1417)

    log(414)