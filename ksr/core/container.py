#!/usr/bin/env python3

"""container.py: KSR wrapper. Stores daemons & GUI."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.6"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

try:
    import RPi.GPIO as GPIO
except ImportError:
    print('Missing module: RPi.GPIO\n'
        + 'Defaulting to Mock.GPIO')
    import Mock.GPIO as GPIO
import sys

from common.gpio_pin import GPIOPin
from common.singleton import Singleton
from core.gui import GUI
from daemon.event_listener import EventListener
from daemon.canbus import CANBus
from daemon.logger import Logger
from PyQt5.QtWidgets import QApplication
from threading import Event


class Container(metaclass = Singleton):
    def __init__(self):
        self._stop = Event()
        
        self.canbus = CANBus()
        self.logger = Logger()
        #self._app = QApplication(sys.argv)
        #self.gui = GUI(self.canbus)
        self.event_listener = EventListener()

        self._daemons = [
            self.event_listener,
            self.canbus,
            self.logger
        ]
        
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(GPIOPin.L_BLINKER_OUTPUT, GPIO.OUT)
        GPIO.setup(GPIOPin.R_BLINKER_OUTPUT, GPIO.OUT)
        GPIO.output(GPIOPin.L_BLINKER_OUTPUT, 0)
        GPIO.output(GPIOPin.R_BLINKER_OUTPUT, 0)

        GPIO.setup(GPIOPin.L_BLINKER_INPUT, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(GPIOPin.R_BLINKER_INPUT, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(GPIOPin.HAZ_INPUT, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        
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
                self._stop.wait(0.01667)
        except KeyboardInterrupt:
            event_handler.bind(Event_.KSR_SHUTDOWN)
        """

        self._stop.wait(10)
        
        print('Exiting KSR')
        
        print('\tStopping daemons')
        for d in reversed(self._daemons):
            if d.is_alive():
                d.stop()
                d.join()
                print('\t\t' + d.name + ' stopped')
        
        print('Done')
        sys.exit(0)   
        
    def stop(self):
        self._stop.set()
        