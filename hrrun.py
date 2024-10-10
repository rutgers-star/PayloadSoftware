import serial
from Logs.errors import ERROR
from Logs.log import log
from time import sleep

log(0)
hex_code = "0xec 0x4 0xfe 0x0 0x4"

# attempt to open serial connection
try:
    serialPort = serial.Serial("/dev/ttyS0",115200)

except Exception:
    raise ERROR(1303, f"failed to open serial port /dev/ttyS0 - {hex_code}")
    
# make packet to send hex values to serial port
packet = bytearray()
arr = hex_code.split(" ")
for item in arr:
    packet.append(int(item, 16))

# write packet to the serial port
while True:
    try:
        serialPort.write(packet)

    except Exception:
        raise ERROR(1303, f"failed to write to serial port /dev/ttyS0 - {hex_code}")
    
    log(303, f"- {hex_code}")

    print(serialPort.read(4))

    sleep(.2)