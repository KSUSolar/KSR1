#!/usr/bin/env python3

"""gui.py: Car dashboard. Displays car telemetry."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.5"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

from canbus import CANBus
from light_controller import LightController
from threading import Event
from tkinter import *


class GUI():
    def __init__(self, stop_: Event, canbus: CANBus, light_controller: LightController):
        self._stop_ = stop_
        self._canbus = canbus
        self._light_controller = light_controller
        
        window = Tk()
        window.title('KSR')
        window.geometry('900x600')
        
        #window.after(17, self._update_widgets)
        
        # Close window on window 'X' clicked or 'ESC' press.
        window.protocol('WM_DELETE_WINDOW', self.close)
        window.bind('<Escape>', self.close)
        
        self._window = window
    
    def start(self):
        while not self._stop_.is_set():
            self._update_widgets()
            self._window.update_idletasks()
            self._window.update()
            self._stop_.wait(0.01667)
        
    def _update_widgets(self):
        return
        
    def close(self):
        self._window.destroy()
        print('GUI window closed')
        self._stop_.set()