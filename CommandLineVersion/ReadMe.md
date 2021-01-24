# CW over CAT for Kenwood TS590SG (command line tools)

This is a first release of my (bare minimum) command-line Python3 utilities to control my Kenwood radio via CAT control (i.e. just one single USB cable between the PC and the radio) and use it to send CW messages.

Note that I am not (yet) skilled in Python. I started this exploiration to see whether my radio could be ultimately controlled by the PC, without ad hoc external interfaces or additional cables running from my PC to the radio. These experiments set the ground for a minimalistic GUI software to have rapid contest operation (inspired by Morse Runner). 


## Required Python modules

The extra module ```PySerial``` has to be (pip3) installed, if not already available in your Python3 environment. On my laptop, I just installed it by pip3:

```> pip3 install pyserial```

See more at <https://pypi.org/project/pyserial/>


## Configuration of the serial interface

The parameters for configuring the (USB) serial port communication with the Kenwood TS590SG,and to specify to which computer port the radio is connected to, can be changed by carefully editing the file ```CWvCAT.py```.

This file contains three variables controlling the name of the PC serial port in use, the debug logging level, and the allowed communication delay between (PC) command and (radio) response. If this delay is set to ```0``` s, the communication does not work correctly, in my own experience.

- ```COMPORT``` (set it, e.g., to ```'COM3'``` on Windows)
- ```DEBUG``` (set it *True* to increase console verbosity)
- ```DELAY```  (set it to, e.g., ```0.15``` seconds)


Please check and edit the serial port parameters - at the begining of the ```initSerialPort()``` function definition.
Their current values work for my setup and radio, but you might want to read the TS590SG manual again and change its USB settings from the radio's menus.


## Actual Scripts

I wrote three Python3 scripts, following the radio's "PC command reference manual (rev. 3)" available for download from Kenwood (https://www.kenwood.com/i/products/info/amateur/pdf/ts590_g_pc_command_en_rev3.pdf). 

- ```readIF.py``` (requires no input arguments)
- ```send.py```   (requires the WPM and the message string) 
- ```stop.py```   (requires no input arguments)

They must be called from the shell (e.g.) as
	```> python3 ./readIF.py```

or as
	```> ./readIF.py```,

if given execution privileges (e.g. by ```chmod +x readIF.py```). In this case, check that the very first line of each script points to your python3 environment path.

The first script (```readIF.py```) simply polls the radio to get its frequency, mode, and transmit status. More information can be in principle extracted. Please refer to the (comprehensive) Kenwood manual entry for the ```IF``` command.

For instance,	```> python3 ./readIF.py``` returns

```
readIF.py v0.1, by MG (iv3ifz)
QRG [kHz]:      10100.007
Mode:           CW
Status:         RX
```


The second script (```send.py```) transfer to the radio a string of characters to be sent automatically via CW on the air (if the radio's VOX is on, of course) at the specified words-per-minute (WPM) speed.

For instance,	```> python3 ./send.py 25 "CQ IV3IFZ TEST"``` almost immediately keys the radio to send the string at 25 words per minute.

The last script (```stop.py```) stops the radio's CW sending, initiated by the previous script.

For instance,	```> python3 ./stop.py``` stops the previous keying if launched quickly enough, while the radio is still keying. 

Note that the radio has a certain buffer to accumulate multiple messages to be automatically sent in CW. I did not yet investigate such a limit. In real life, a ```send.py``` command will wait until the radio has finished transmitting the previous message (or until its status is still "transmitting"). This is important because the setting of WPM would otherwise alter the currently sent message.
By this arrangement, you can send (e.g.) IV3IFZ at 20WPM and then 5NN at 35WPM (remember this works only if VOX is turned on, otherwise the radio won't be in transmit mode).

## Get in touch

If need more information, do not hesitate to contact me (QRZ.com or Google).

