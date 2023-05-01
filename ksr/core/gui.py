#!/usr/bin/env python3

"""gui.py: Car dashboard. Displays car telemetry."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.7"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import threading
import time

from tkinter import *

from daemons.canbus import CANBus

class GUI():
    def __init__(self):
        self._should_stop = threading.Event()
        
        window = Tk()
        window.title('KSR')
        window.geometry('900x600')
        window.configure(bg='black')
        
        # Close window on window 'X' clicked or 'ESC' press.
        window.protocol('WM_DELETE_WINDOW', self.stop)
        window.bind('<Escape>', self.stop)
        
        self._window = window
        self._canbus = CANBus()
    
    def start(self):
        while not self._should_stop.is_set():
            start_time = time.time_ns() / 1000000000
            self._update()
            self._window.update()
            end_time = time.time_ns() / 1000000000
            time_taken = end_time - start_time
            time.sleep(0.1667 - time_taken)
        self._close()
        
    def _update(self):
        for i, (key, value) in enumerate(self._canbus.data.items()):
            label = Label(self._window, text=f'{key}: {value}', 
                          bg='black', fg='white', font=('Helvetica', 24), anchor='w')
            label.grid(row=i, column=0)
        
    def _close(self):
        if not self.is_destroyed:
            self._window.destroy()
            print('GUI Closed')
        
    def stop(self):
        self._should_stop.set()
        
    @property
    def is_destroyed(self):
        if self._window.winfo_exists():
            return False
        return True
        
        