# Below, the callback functions for the MikeRunner GUI.
#

def readIF(ser):
    #------------------------------------------------------------------------------
    log("Sending IF command...")
    #------------------------------------------------------------------------------
    data = send_command(ser, 'IF;', 38)
    # Now the response from the radio is parsed...
    tmp  = data.decode('ascii')
    freq = float(tmp[2:13])/1000. # This is the frequency in kHz.
    tmp  = int(tmp[28])           # This is current state TX/RX.
    #Status = ['RX', 'TX']
    #txstatus = Status[tmp]
    #------------------------------------------------------------------------------
    log("IF: success!")
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    log("Sending MD command...")
    #------------------------------------------------------------------------------
    data = send_command(ser, 'MD;', 4)
    # Now the response from the radio is parsed...
    tmp  = data.decode('ascii')
    #radioMode = ["none", "LSB", "USB", "CW", "FM", "AM", "FSK", "CW-R", "none.", "FSK-R"]
    radioMode = ["none", "PH", "PH", "CW", "FM", "PH", "DG", "CW", "none.", "DG"]
    mode = int(tmp[2:3])
    #------------------------------------------------------------------------------
    log("MD: success!")
    #------------------------------------------------------------------------------
    return f'{freq:.0f}', radioMode[mode] # both are strings

#------------------------------------------------------------------------------

def stop(ser):
    #------------------------------------------------------------------------------
    log("Sending KY STOP command...")
    #------------------------------------------------------------------------------
    data = send_command(ser, 'KY0;', 0)
    #------------------------------------------------------------------------------
    log("KY STOP: success!")
    #------------------------------------------------------------------------------

def halt_sending(event=None):
    stop(ser)
#------------------------------------------------------------------------------

def send(ser, nwpm, inp):
    wpm = f'{nwpm:03d}'
    #------------------------------------------------------------------------------
    log("Checking if TX...")
    #------------------------------------------------------------------------------
    while True :
        log("Sending IF command...")
        data = send_command(ser, 'IF;', 38)
        log("IF: success!")
        # Now the response from the radio is parsed...
        tmp  = data.decode('ascii')
        RX   = int(tmp[28])           # This is current state TX/RX.
        if not RX :
            break
        print('Still TX: waiting...')
        time.sleep(.100)
    #------------------------------------------------------------------------------
    log("Radio is now in RX...")
    #------------------------------------------------------------------------------

    # Beware of artifacts!
    # I set the WPM only if the radio is not currently sending a message!
    # Otherwise the new WPM setting will immediately affect what it is
    # being sent. This would not be the intened behavior.
    # Therefore, without VOX your radio will sound odd.

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


#------------------------------------------------------------------------------

def CQ(event=None): #set event to None to take the key argument from .bind
    log('Calling CQ...') #this will output in the shell
    nwpm = int(wpm.get())
    send(ser, nwpm, cqmessage)
    callsign.set('')
    CL.focus_set()
    #CL.delete(0, END)
    #CL.insert(0, "")
#------------------------------------------------------------------------------

def NR(event=None): #set event to None to take the key argument from .bind
    log('Repeating 5NN and NR...') #this will output in the shell
    nwpm    = int(wpm.get())
    mwpm    = int(wpm_5nn)
    send(ser, mwpm, sent_rst)
    send(ser, nwpm, cut_numbers(mynumber.get()))
    NRN.focus_set()

#------------------------------------------------------------------------------

def TU(event=None): #set event to None to take the key argument from .bind
    log('Sending TU...') #this will output in the shell
    nwpm    = int(wpm.get())
    send(ser, nwpm, "TU")
    CL.focus_set()

#------------------------------------------------------------------------------

def MY(event=None): #set event to None to take the key argument from .bind
    log('Sending my callsign...') #this will output in the shell
    nwpm    = int(wpm.get())
    send(ser, nwpm, mycallsign)
    CL.focus_set()

#------------------------------------------------------------------------------

def DE(event=None): #set event to None to take the key argument from .bind
    log('Sending DE + my callsign...') #this will output in the shell
    nwpm    = int(wpm.get())
    send(ser, nwpm, "DE " + mycallsign)
    CL.focus_set()

#------------------------------------------------------------------------------

def HIS(event=None): #set event to None to take the key argument from .bind
    log('Sending his callsign...') #this will output in the shell
    nwpm    = int(wpm.get())
    send(ser, nwpm, callsign.get())
    CL.focus_set()

#------------------------------------------------------------------------------

def B4(event=None): #set event to None to take the key argument from .bind
    log('Sending B4 TU...') #this will output in the shell
    nwpm    = int(wpm.get())
    send(ser, nwpm, "B4 TU")    

#------------------------------------------------------------------------------

def QM(event=None): #set event to None to take the key argument from .bind
    log('Sending ?...') #this will output in the shell
    nwpm    = int(wpm.get())
    send(ser, nwpm, "?")
    CL.focus_set()

#------------------------------------------------------------------------------

def NIL(event=None): #set event to None to take the key argument from .bind
    log('Sending NIL...') #this will output in the shell
    nwpm    = int(wpm.get())
    send(ser, nwpm, "NIL")    
    CL.focus_set()

#------------------------------------------------------------------------------

def cl_enter(event=None): #set event to None to take the key argument from .bind
    log('Pressed ENTER on his callsign...')
    nwpm    = int(wpm.get())
    mwpm    = int(wpm_5nn)
    if "?" in callsign.get() :
        log("Asking to repeat...")
        send(ser, nwpm, callsign.get())    
    else : 
        log("Sending 5NN and NR...")
        send(ser, nwpm, callsign.get())
        send(ser, mwpm, sent_rst)
        send(ser, nwpm, cut_numbers(mynumber.get()))
        # REPEAT THE NUMBER HERE???
        rst.set(sent_rst)
        NRN.focus_set()

#------------------------------------------------------------------------------

def logentry(event=None): #set event to None to take the key argument from .bind
    log('Adding a log entry...') #this will output in the shell

    #                              --------info sent------- -------info rcvd--------
    #QSO:  freq mo date       time call          rst exch   call          rst exch   t
    #QSO: ***** ** yyyy-mm-dd nnnn ************* nnn ****** ************* nnn ****** n
    #QSO:  3799 PH 1999-03-06 0711 HC8N           59 700    W1AW           59 CT     0
    #QSO:  3799 PH 1999-03-06 0712 HC8N           59 700    N5KO           59 CA     0

    freq, mode = readIF(ser)
    utc        = datetime.utcnow()
    output     = utc.strftime('%Y-%m-%d %H%M')

    rxnr = int(nr.get())
    rxnr = f'{rxnr:03d}'

    n = len(freq)
    logentry = 'QSO:' + ' '*(6-n) + freq + ' ' + mode + ' ' + output + ' ' + mycallsign.upper();
    n = len(logentry)
    logentry = logentry + ' '*(44-n) + sent_rst + ' ' + mynumber.get() + '    ' + callsign.get().upper()
    n = len(logentry)
    logentry = logentry + ' '*(69-n) + rst.get() + ' ' + rxnr + '    '
    n = len(logentry)
    logentry = logentry + ' '*(80-n) + '0' + '\n'
 
    log("Writing to disk: " + logfile_name)

    with open(logfile_name, "a") as myfile:
        myfile.write(logentry)

    nwpm    = int(wpm.get())
    send(ser, nwpm, "TU")    
    send(ser, nwpm, mycallsign)    

    logentry = ""
    callsign.set('')
    rst.set('')
    nr.set('')
    tmp = int(mynumber.get()) + 1
    mynumber.set(f'{tmp:03d}')
   
    CL.focus_set()

#------------------------------------------------------------------------------

def LOGF():
    global logfile_name    # Needed to modify global copy of globvar
    global bFILE
    logfile_name = asksaveasfilename(title='Choose logfile to append to...', initialdir='./', confirmoverwrite=False)
    bFILE['text'] = os.path.basename(logfile_name)
    CL.focus_set()

#------------------------------------------------------------------------------

def center_window(width=300, height=200):
    # get screen width and height
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/3) - (height/3)
    master.geometry('%dx%d+%d+%d' % (width, height, x, y))

#------------------------------------------------------------------------------

def focus_rst(event):
    RST.focus_set()
    return("break")

#------------------------------------------------------------------------------
 
def cut_numbers(istr):
    ostr = ''.join(istr)
    #print(ostr)
    #ostr = ostr.replace('1', 'A')
    #ostr = ostr.replace('2', 'U')
    #ostr = ostr.replace('3', 'V')
    #ostr = ostr.replace('3', 'V')
    ostr = ostr.replace('5', 'E')
    #ostr = ostr.replace('7', 'G')
    #ostr = ostr.replace('8', 'D')
    ostr = ostr.replace('9', 'N')
    ostr = ostr.replace('0', 'T')
    return ostr

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
