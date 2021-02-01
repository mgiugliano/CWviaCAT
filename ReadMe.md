# CW over CAT for Kenwood TS590SG

**UPDATE**: First developed under macOs, the (command line) software works flawlessly under Windows. The GUI also works but the window is wrongly sized under Windows, presumably depending on my original screen resolution. I will try to tweak Tkinker's settings to solve the bug. 

## Introduction

I am a HAM radio operator and I am currently studying wireless telegraphy, known as CW (https://en.wikipedia.org/wiki/Wireless_telegraphy). I am still as novice and during the last weeks, while enjoying the intermediate-level course from CW Academy (https://cwops.org/cw-academy/), my instructor suggested to use Morse Runner. This is a Windows software (http://www.dxatlas.com/morserunner/) that simulates quite accurately the experience of "radio contesting" (https://en.wikipedia.org/wiki/Contesting).

During a contest, operators normally use a software to log their contacts. The very same software is sometimes used to control automatically the "keyer" of the radio, so that manually sending CW is replaced by computer automation.
While having a "computer sending CW" is sometimes the theme of heated discussions among CW practitioners, I liked the fun of Morse Runner and I thought of giving contesting a go in the near future. Last year, I enjoyed participating to the 2020 "40-80" contest by the Italian Amateur Association (http://www.ari.it/contest-hf/contest-4080.html) and ranked 50% of all the (81) participants in my category.

From my initial explorations, I found that modern logging software for ham radio (https://n1mmwp.hamdocs.com , https://www.ik3qar.it/software/qartest/en/ , etc.) cannot control my radio directly. A specific interface (i.e. an additional external keyer) has to be acquired or built (http://nanokeyer.wordpress.com). So, it seems that connecting my radio to the computer by a single USB cable is not enough to have the computer sending CW automatically.

However, some radios (KX3, Flex, and indeed my own Kenwood too) can be somehow controlled via the so-called CAT standard (https://en.wikipedia.org/wiki/Computer_Aided_Transceiver) to send CW messages.

Out of curiosity, I spent a couple of weekends learning how to communicate over the (USB) serial cable from my computer to the radio and I successfully built elementary software to prove the point: you can easily make the TS590SG send CW code on the air.

This project on GitHub is to share what I did, hoping that others might find it useful. I am sharing command-line utilities as well as a very plain and basic graphical user interface (GUI).

