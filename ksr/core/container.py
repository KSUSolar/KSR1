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

from common.event import Event_
from common.gpio_pin import GPIOPin
from core import event_handler
from core.gui import GUI
from daemon.event_listener import EventListener
from daemon.canbus import CANBus
from daemon.logger import Logger
from PyQt5.QtWidgets import QApplication
from threading import Event


class Container:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Container, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self._stop = Event()
        
        self.canbus = CANBus()
        self.logger = Logger(self.canbus)
        #self._app = QApplication(sys.argv)
        #self.gui = GUI(self.canbus)
        self.event_listener = EventListener(self.canbus)

        self._threads = [
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
    
        print('\tStarting threads')
        for t in self._threads:
            t.start()
            print('\t\t' + t.name + ' started')
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
        
        print('\tClosing threads')
        for t in reversed(self._threads):
            print('\t\t' + t.name + ' stopping')
            t.stop()
            try:
                t.join()
            except Exception as e:
                print(e)
        
        print('Done')
        sys.exit(0)   
        
    def stop(self):
        self._stop.set()
        