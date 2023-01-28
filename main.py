#!/usr/bin/env python3

"""main.py: Main entrypoint for KSR1 program. Creates all threads."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.5"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import sys
from threading import Event

from canbus import CANBus
from gui import GUI
from light_controller import LightController
from logger import Logger

def stop():
    print('Exiting KSR')
    
    stop_.set()
    
    print('\tClosing threads')
    for t in reversed(threads):
        print('\t\t' + t.name + ' stopping')
        try:
            t.join()
        except:
            pass
    
    print('\tDone')
    sys.exit(0)

stop_ = Event()

canbus = CANBus(stop_)
light_controller = LightController(stop_)
logger = Logger(stop_, canbus)
gui = GUI(stop_, canbus, light_controller)

threads = [
    canbus,
    light_controller,
    logger
]

if __name__ == '__main__':
    print('Booting up KSR')
    try:
        print('\tStarting threads')
        for t in threads:
            t.start()
            print('\t\t' + t.name + ' started')
        
        print('\tOpening GUI window\nStartup finished')
        gui.start() # Blocks until gui closed.
    except KeyboardInterrupt:
        pass
        
    stop()