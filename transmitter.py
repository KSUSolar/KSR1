#!/usr/bin/env python3

"""transmitter.py: Transmits canbus.py data over radio."""

__author__      = "Aaron Harbin"
__copyright__   = ""
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.3"
__maintainer__  = ""
__email__       = ""
__status__      = "Development"

import digitalio
import board
import busio
import adafruit_rfm9x

def transmitString(tString):
    CS = digitalio.DigitalInOut(board.D2)
    RESET = digitalio.DigitalInOut(board.D26)
    spi = busio.SPI(clock=board.D21, MOSI=board.D20, MISO=board.D19)
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0) # 10mhz is the standard baudrate (baudrate=1000000

    # Should be as simple as using this command to send
    rfm9x.send(tString.encode()) # Maximum packet size is 60 BYTES.  So 60 characters maximum

    # Should be as simple as using this command to recieve
    #print(rfm9x.receive(timeout=5.0)) # this command will wait 5 seconds to try and recieve a packet before timing out.
    
if __name__ == '__main__':
    transmitString(input('Enter the string to transmit: '))