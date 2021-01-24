#!/usr/local/bin/python3

# stop.py
#
# Jan 24th 2021 - (c) Michele Giugliano

from CWvCAT import *

NAME = 'stop.py'

ser = initSerialPort(COMPORT)

#------------------------------------------------------------------------------
log("Sending KY STOP command...")
#------------------------------------------------------------------------------
data = send_command(ser, 'KY0;', 0)
#------------------------------------------------------------------------------
log("KY STOP: success!")
#------------------------------------------------------------------------------
ser.close()

print(NAME + " v" + VERSION + ", by " + AUTHOR)
if len(data)==0 :
	print("Stopped CW sending.")

