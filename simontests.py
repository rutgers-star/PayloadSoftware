from dce_control import *

actual=b'\x1a\xcf\x04\x89\x00\x10\x00\x08dp\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfb'
print(len(actual)==6+16+1)
actual=bytes.hex(actual)

#actual="1acf04690010002161d40000000000000000000000008d" #speed
print(int(actual, 16))
print(actual)
wheel_arr = [actual[12:20], actual[20:28], actual[28:36], actual[36:44]]
print(wheel_arr)

wheel_arr = [actual[12:20], actual[20:28], actual[28:36], actual[36:44]]
for i in range(len(wheel_arr)):
    wheel_arr[i] = convert_from_hex(wheel_arr[i], universal["TORQUE_READ_CONV"][0])
    
print(wheel_arr)

print(convert_from_hex("05F5E100", universal["TORQUE_WRITE_CONV"][0]))


