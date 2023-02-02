#!/usr/bin/env python3

"""gui.py: Car dashboard. Displays car telemetry."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.6"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import time
import threading

from tkinter import *


class GUI():
    #_instance = None
    
    #def __new__(cls, *args, **kwargs):
    #    if cls._instance is None:
    #        cls._instance = super(GUI, cls).__new__(cls)
    #        cls._instance.__init__(*args, **kwargs)
    #    return cls._instance
    
    def __init__(self):
        self.is_destroyed = False
        self._stop = threading.Event()
        
        window = Tk()
        window.title('KSR')
        window.geometry('900x600')
        
        # Close window on window 'X' clicked or 'ESC' press.
        window.protocol('WM_DELETE_WINDOW', self.close)
        window.bind('<Escape>', self.close)
        
        self._window = window
    
    def start(self):
        while not self._stop.is_set():
            self._update_widgets()
            self._window.update_idletasks()
            self._window.update()
            time.sleep(0.01667)
        
    def _update_widgets(self):
        return
        
    def close(self, *args):
        self._stop.set()
        self._window.destroy()
        self.is_destroyed = True
        
    @property
    def is_closed(self):
        return self._stop.is_set()