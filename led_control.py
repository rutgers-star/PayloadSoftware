#!/usr/bin/env python

"""
A module to control the LED for the camera
"""

from Logs.log import log
from Logs.errors import ERROR
import RPi.GPIO as GPIO

author="Shreyas Bhatkande"
credits=["Shreyas Bhatkande"]
creation_date="2/22/2025"

pin = 17

def init_led(pin: int = 17):
    """
    Initialize the LED
    
    
    """
    log(500) #Setting up LED

    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    except Exception:
        raise ERROR(1500)
        

    log(501) #LED initialized

def led_on():
    """
    Turn the LED on
    """
    log(502) #Turning on LED
    GPIO.output(pin, GPIO.HIGH)

def led_off():
    """
    Turn the LED off 
    """
    log(503) #Turning off LED
    GPIO.output(pin, GPIO.LOW)

def close_led():
    """
    Reset the GPIO pins
    """

    log(504)
    GPIO.cleanup()  
