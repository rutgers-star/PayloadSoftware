#!/usr/bin/env python

"""
A module to control and access the camera
"""
import subprocess

from Logs.log import log
from Logs.errors import ERROR

author="Serene Siu"
credits=["Serene Siu"]
creation_date="10/4/24"

camlog=open("camlog.txt",'w')

def init_camera():
    """
    Camera Start Up
    """

    log(400)

    try:
        cam=subprocess.Popen(["/usr/local/bin/libcamera-vid", "-t 20000", "--nopreview", "--width", "960", "--height","540","--vflip","--saturation","0","--save-pts","camtimes.txt","--exposure","long","--framerate","24","-o","sloshing.h264"], text=True, stderr=camlog)
    except Exception:
        raise ERROR(1400, "fail to startup camera")

    log(401)

def close_camera():
    """
    Camera Shut Down
    """
    log (402)
    camlog.close()
    log(403)