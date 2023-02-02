#!/usr/bin/env python3.10

"""container.py: KSR wrapper. Stores daemons & GUI."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.6"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import sys
from common.event import Event_

from common.gpio_pin import GPIOPin
from common.singleton import Singleton
from core import event_handler
#from core.gui import GUI
from daemons.gpio_listener import GPIOListener
from daemons.canbus import CANBus
from daemons.logger import Logger
#from PyQt5.QtWidgets import QApplication
from threading import Event


class Container(metaclass = Singleton):
    def __init__(self):
        self._stop_ = Event()
        #self._app = QApplication(sys.argv)
        
        self.canbus = CANBus()
        self.logger = Logger()
        self.event_listener = GPIOListener()
        #self.gui = GUI(self.canbus)

        self._daemons = [
            self.event_listener,
            self.canbus,
            self.logger
        ]
        
    def start(self):
        print('Booting up KSR')
    
        print('\tStarting daemons')
        for d in self._daemons:
            if not d.is_disabled:
                d.start()
                print('\t\t' + d.name + ' started')
        print('Done')
        
        """
        try:
            print('\tOpening GUI window\nStartup finished')
            self.gui.show_()
            while not self._stop.is_set():
                self.gui._update()
                self._stop_.wait(1 / 60)
        except KeyboardInterrupt:
            event_handler.bind(Event_.KSR_SHUTDOWN)
        """

        self._stop_.wait(10)
        event_handler.bind_async(Event_.KSR_SHUTDOWN)
        
    def stop(self):
        print('Exiting KSR')
        
        self._stop_.set()
        
        print('\tStopping daemons')
        for d in reversed(self._daemons):
            if d.is_alive():
                d.stop()
                d.join()
                print('\t\t' + d.name + ' stopped')
        
        print('Done')
        sys.exit(0)