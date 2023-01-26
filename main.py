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
from canbus import CanBus
from light_controller import LightController
from logger import Logger
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    canbus = CanBus()
    canbus.start()
    
    light_controller = LightController()
    light_controller.start()

    logger = Logger(canbus)
    canbus.start()
    
    app = QApplication(sys.argv)
    gui = GUI(canbus, light_controller)
    app.exec()

def quit(canbus: CanBus, light_controller: LightController, logger: Logger):
    canbus.stop()
    canbus.join()
    light_controller.stop()
    light_controller.join()
    logger.stop()
    logger.join()
    sys.exit(0)