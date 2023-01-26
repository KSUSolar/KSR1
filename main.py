#!/usr/bin/env python3

"""main.py: Main entrypoint for KSR1 program. Sets up required threads."""

__author__      = "Daniel Tebor"
__copyright__   = ""
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.3"
__maintainer__  = ""
__email__       = ""
__status__      = "Development"

import sys

from gui import GUI
from canbus import CanBus
from light_controller import LightController
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    canbus = CanBus()
    canbus.start()
    
    light_controller = LightController()
    light_controller.start()
    
    app = QApplication(sys.argv)
    gui = GUI(canbus, light_controller)
    app.exec()

def quit(canbus, light_controller):
    canbus.stop()
    canbus.join()
    light_controller.stop()
    light_controller.join()
    sys.exit(0)