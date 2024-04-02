import os
import subprocess


########### CAMERA STARTUP CODE BEGIN ##############
#os.system("libcamera-vid -t 10000  --nopreview --width 640 --height 480 --sharpness 1.5 --exposure long --framerate 5 --codec mjpeg -o test.mjpeg")
#os.system("libcamera-vid -t 10000   --width 640 --height 480 --sharpness 1.5 --exposure long --framerate 5 --codec mjpeg -o test.mjpeg &",stdout="camlog.txt",stderr=STDOUT)
#subprocess.run("libcamera-vid -t 10000   --width 640 --height 480 --sharpness 1.5 --exposure long --framerate 5 -o test.h264 > camlogos.txt &",stdout="camlog.txt",stderr=stdout)
#camlog=subprocess.run(["libcamera-vid", "-t 10000", "--width 640", "--height 480", "--sharpness 1.5", "--exposure long", "--framerate 5", "-o test.h264," "> camlogos.txt," "&"], capture_output=True)
#camlog=subprocess.run(["libcamera-vid -t 10000 --width 640 --height 480 --vflip --sharpness 1.5 --exposure long --framerate 5 -o test.h264 &"], capture_output=True)
########### CAMERA STARTUP CODE END ##############

#camlog=subprocess.run(["ls","-al"])
#camlog=subprocess.run(["ps", "-ae", "|", "grep","thonny"])
#camlog=subprocess.run(["ps", "-ae",],capture_output=True, text=True)
#camlog=subprocess.run(["ps", "-ae"])
#camlog=subprocess.run(["libcamera-vid","-t 1000","'--width 640'"])
#camlog=subprocess.run(["libcamera-vid", "-t 10000", "'--width 640'", "'--height 480'","'--vflip'", "'--sharpness 1.5'", "'--exposure long'", "'--framerate 5'", "'-o test.h264'", "'> camlogos.txt'", "'&'"], capture_output=True, text=True)
#camlog=subprocess.run(["libcamera-vid", "-t 5000", "'--width 640'", "'--height 480'","'--vflip'", "'--sharpness 1.5'", "'--exposure long'", "'--framerate 5'", "-o test.h264"], capture_output=True, text=True)
#camlog=subprocess.run(["libcamera-vid", "-t 5000", "--framerate", "5", "-o test.h264"], capture_output=True, text=True)
#camlog=subprocess.run(["libcamera-vid", "-t 5000", "--width", "640", "--height","480","--vflip","--sharpness","1.5","--exposure","long","--framerate","5","-o","test.h264"], capture_output=True, text=True)
#camlog=subprocess.run(["libcamera-vid", "-t 5000", "--width", "640", "--height","480","--vflip","--sharpness","1.5","--exposure","long","--framerate","5","-o","test.h264"], capture_output=True, text=True)
camlog=open("camlog.txt",'w')
#cam=subprocess.Popen(["/usr/local/bin/libcamera-vid", "-t 5000", "--width", "640", "--height","480","--vflip","--sharpness","1.5","--exposure","long","--framerate","5","-o","test.h264"], text=True, stderr=camlog)
cam=subprocess.Popen(["/usr/local/bin/libcamera-vid", "-t 20000", "--width", "640", "--height","480","--vflip","--saturation","0","--exposure","long","--framerate","5","-o","test.h264"], text=True, stderr=camlog)



#print()
#print()
#print(camlog.stdout)
#print()
#print()
#print(camlog.stderr)
camlog.close()
