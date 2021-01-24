#!/usr/local/bin/python3

# stop.py
#
# Jan 24th 2021 - (c) Michele Giugliano

from CWvCAT import *
import sys

NAME = 'send.py'

#------------------------------------------------------------------------------
if len(sys.argv) < 3 :
    print("USAGE " + sys.argv[0] + " WPM(e.g 24) message(between double quotes)")
    exit(1)

if len(sys.argv[2]) > 47 :
    print("Message too long (empirically determined)!")
    exit(1)

if len(sys.argv[1]) > 3 :
    print("Wrong WPM format: it should be as 24 or 024!")
    exit(1)
#------------------------------------------------------------------------------
wpm = sys.argv[1]   # speed in words per minute (as e.g. 025 or 008)
inp = sys.argv[2]   # text of the message to be sent
#------------------------------------------------------------------------------

ser = initSerialPort(COMPORT)

#------------------------------------------------------------------------------
log("Checking if TX...")
#------------------------------------------------------------------------------
while True :
    log("Sending IF command...")
    data = send_command(ser, 'IF;', 38)
    log("IF: success!")
    # Now the response from the radio is parsed...
    tmp  = data.decode('ascii')
    TX   = int(tmp[28])           # This is current state TX/RX.
    if not TX :
        break
    print('Still TX: waiting...')
    time.sleep(.100)
#------------------------------------------------------------------------------
log("Radio is now in RX...")
#------------------------------------------------------------------------------

# I set the WPM only if the radio is not currently sending a message!
# Otherwise the new WPM setting will immediately affect what it is
# being sent. This would not be the intened behavior.

#------------------------------------------------------------------------------
log("Setting WPM...")
#------------------------------------------------------------------------------
# Let's first set the radio at the desired keying speed
if wpm[0] == '0' :
    out = 'KS' + wpm + ';'
else :
    out = 'KS' + '0' + wpm + ';'
send_command(ser, out, 0)
#------------------------------------------------------------------------------
log("WPM: success!")
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
log("Transfering your message to the radio...")
#------------------------------------------------------------------------------
# Now let's encode the message to be sent at such a speed
N = len(inp)        # This is the length of the input string

if N <= 24 :        # When below the serial command length limit
    n   = 24 - N    # calculate the proper number of "filler" spaces
    out = 'KY ' + inp.upper() + ' '*n + ';'  # and prepare the command
    send_command(ser, out, 0) # send the command to the radio
    #print(out)
else :              # If instead the length is too long, it must be splitted
    #--------------------------------------------------------------------------
    log("Message needs to be broken in chunks...")
    #--------------------------------------------------------------------------
    k = 0           # Auxiliary variable for the current 'chunk'
    M   = 24
    while M<N :     # Repeat until we exhaust the length of the original chars
        tmp = inp[k:M]
        n   = 24 - len(tmp)
        out = 'KY ' + tmp.upper() + ' '*n + ';'
        send_command(ser, out, 0) # send the command to the radio
        #print(out)
        k = M
        M   = min([24+k, N])

    tmp = inp[k:N]
    n   = 24 - len(tmp)
    out = 'KY ' + tmp.upper() + ' '*n + ';'
    send_command(ser, out, 0)  # send the command to the radio
    #print(out)
#------------------------------------------------------------------------------
log("Message transferred correctly...")
#------------------------------------------------------------------------------

ser.close()

print(NAME + " v" + VERSION + ", by " + AUTHOR)
