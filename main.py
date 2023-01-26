#!/usr/bin/env python3

"""main.py: Main entrypoint for KSR1 program. Sets up required threads."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.3"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import sys

from gui import GUI
from canbus import CANBus
from light_controller import LightController
from logger import Logger
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
canbus = CANBus()
light_controller = LightController()
logger = Logger(canbus)

if __name__ == '__main__':
    canbus.start()
    light_controller.start()
    logger.start()
    gui = GUI(canbus, light_controller)
    app.exec()

def quit():
    print('quiting')
    
    logger.stop()
    if logger.is_alive():
        logger.join()

    light_controller.stop()
    if light_controller.is_alive():
        light_controller.join()

    canbus.stop()
    if canbus.is_alive():
        canbus.join()

    sys.exit(0)