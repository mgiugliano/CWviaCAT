#!/usr/local/bin/python3

# MikeRunner.py
#
# Jan 24th 2021 - (c) Michele Giugliano

#------------------------------------------------------------------------------
# CHANGE THESE SETTINGS ACCORDING TO YOUR SETUP AND PREFS
#------------------------------------------------------------------------------
logfile_name    = '/Users/michi/Desktop/AUTO_DELETE/ciao.txt';
#
mycallsign      = 'iv3ifz'
cqmessage       = 'cq iv3ifz test' 
wpm_default     = '25'
wpm_5nn         = '25'		   # This requires the the VOX is on, so that the 
							   # radio is currently really transmitting. If u
							   # are just testing beware of artifacts... (see send())
sent_number     = '001'        # Starting string, containing the NR to be sent.
sent_rst        = '5NN'        # Default sent RST report...
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

NAME   = 'MikeRunner.py'
HEIGHT = 3  # height of the buttons
WIDTH  = 5  # width of the buttons

import os as os                 # Useful for inferring log file "basename"
from datetime import datetime   # Required to get the current UTC time
from tkinter import *           # Imports everything from the tkinter lib
from tkinter.filedialog import asksaveasfilename
import tkinter.font as font

from CWvCAT import *            # Contains serial CAT control primitives

ser    = initSerialPort(COMPORT) # Let's open the serial port...

exec(open("./MikeRunner_helper.py").read()) # All the callbacks are defined hr.

#------------------------------------------------------------------------------
master = Tk(className='MikeRunner - v 0.01') # It creates the main GUI window.
#master.geometry("425x290")                   # It sets size only.
center_window(425, 290)                      # It sets both position and size.
master.resizable(False, False)               # It prevents from resizable.

#------------------------------------------------------------------------------
freq     = StringVar()  # Contains the working frequency [kHz]
wpm      = StringVar()  # Contains the word-per-minute setting
mynumber = StringVar()  # Contains the sent NR (incrementing at every QSO...)
callsign = StringVar()  # Contains the received corresponder's call
rst      = StringVar()  # Contains the received RST
nr       = StringVar()  # Contains the received NR
#------------------------------------------------------------------------------
# DEFAULT VALUES
#------------------------------------------------------------------------------
wpm.set(wpm_default)
mynumber.set(sent_number)
#------------------------------------------------------------------------------

myFont0 = font.Font(family='Helvetica', size=15, weight="bold")
myFont1 = font.Font(family='Helvetica', size=25, weight="bold")
myFont2 = font.Font(family='Helvetica', size=30, weight="bold")

# CREATION AND DEFINITION OF THE GUI OBJECTS
canvas = Canvas(master, background="black")
btn_fr = Frame(master, background="black")

canvas.pack(side="top",    fill="both", expand=False)
btn_fr.pack(side="bottom", fill="both", expand=False)

#------------------------------------------------------------------------------
# ENTRY FIELDS CREATION AND ATTRIBUTES
#------------------------------------------------------------------------------
# RECEIVED CALLSIGN
# RECEIVED RST (automatically filled it, but modifiable on-the-fly, if needed)
# RECEIVED NR
CL  = Entry(canvas, textvariable=callsign, font=myFont2, justify="left", width=14, bg="white", fg="black", bd=3, highlightcolor="red")
RST = Entry(canvas, textvariable=rst,      font=myFont2, justify="left", width=4,  bg="white", fg="black", bd=3, highlightcolor="red")
NRN = Entry(canvas, textvariable=nr,       font=myFont2, justify="left", width=4,  bg="white", fg="black", bd=3, highlightcolor="red")
#
# WORD-PER-MINUTE SPEED OF KEYING
# VALUE OF THE "SENT NR" TO BE NEXT SENT
WPM  = Entry(btn_fr, textvariable=wpm,      font=myFont0, justify="center", width=1, bg="white", fg="black", bd=3, highlightcolor="red")
MYNR = Entry(btn_fr, textvariable=mynumber, font=myFont0, justify="center", width=1, bg="white", fg="black", bd=3, highlightcolor="red")
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# BUTTONS CREATION AND ATTRIBUTES 
#------------------------------------------------------------------------------
bCQ  = Button(btn_fr, text = 'CQ',    command = CQ,  height = HEIGHT, width = WIDTH, font=myFont1)
bNR  = Button(btn_fr, text = '#',     command = NR,  height = HEIGHT, width = WIDTH, font=myFont1)
bTU  = Button(btn_fr, text = 'TU',    command = TU,  height = HEIGHT, width = WIDTH, font=myFont1)
bMY  = Button(btn_fr, text = '<my>',  command = MY,  height = HEIGHT, width = WIDTH, font=myFont1)
bHIS = Button(btn_fr, text = '<his>', command = HIS, height = HEIGHT, width = WIDTH, font=myFont1)
bB4  = Button(btn_fr, text = 'B4',    command = B4,  height = HEIGHT, width = WIDTH, font=myFont1)
bQM  = Button(btn_fr, text = '?',     command = QM,  height = HEIGHT, width = WIDTH, font=myFont1)
bNIL = Button(btn_fr, text = 'NIL',   command = NIL, height = HEIGHT, width = WIDTH, font=myFont1)
bDE  = Button(btn_fr, text = 'DE <my>',  command = DE,   height = HEIGHT-2, width = WIDTH, font=myFont0)
bFILE= Button(btn_fr, text = 'Log file', command = LOGF, height = HEIGHT-2, width = WIDTH, font=myFont0)
#
bFILE['text'] = os.path.basename(logfile_name)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# LAYOUT OF EACH ELEMENT OF THE GUI  
#------------------------------------------------------------------------------
CL.grid(  row=1, column=1, sticky="ew")
RST.grid( row=1, column=2, sticky="ew")
NRN.grid( row=1, column=3, sticky="ew")
#
bCQ.grid( row=0, column=1, sticky="ew")
bNR.grid( row=0, column=2, sticky="ew")
bTU.grid( row=0, column=3, sticky="ew")
bMY.grid( row=0, column=4, sticky="ew")
#
bHIS.grid(row=1, column=1, sticky="ew")
bB4.grid( row=1, column=2, sticky="ew")
bQM.grid( row=1, column=3, sticky="ew")
bNIL.grid(row=1, column=4, sticky="ew")
#
bFILE.grid(row=2, column=1, sticky="ew")
WPM.grid(row=2, column=2, sticky="ew")
MYNR.grid(row=2, column=3, sticky="ew")
bDE.grid(row=2, column=4, sticky="ew")
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# KEYBOARD SHORT CUT
#------------------------------------------------------------------------------
master.bind('<F1>', CQ) #binds 'F1'
master.bind('<F2>', NR) #binds 'F1'
master.bind('<F3>', TU) #binds 'F1'
master.bind('<F4>', MY) #binds 'F1'

master.bind('<F5>', HIS) #binds 'F1'
master.bind('<F6>', B4) #binds 'F1'
master.bind('<F7>', QM) #binds 'F1'
master.bind('<F8>', NIL) #binds 'F1'
master.bind('<Escape>', halt_sending)
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# DESIRED ENTRY-FIELDS RESPONSE TO PRESSING ENTER OR TAB
#------------------------------------------------------------------------------
CL.bind('<Return>', cl_enter)  # When focused on the received callsign, pressing
                               # Enter initiate the exchange of RST and NR
NRN.bind('<Tab>', focus_rst)   # When focused on the received NR, pressing Tab 
                               # focuses back the RST entry field.
NRN.bind('<Return>', logentry) # When focused on the received NR, pressing Enter
                               # completes the exchange and logs the QSO on disk. 
#
CL.focus_set()                 # At start-up, focus the callsign entry field..
#------------------------------------------------------------------------------

master.mainloop()

