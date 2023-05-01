#!/usr/bin/env python3

"""container.py: KSR wrapper. Stores daemons & GUI."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.7"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import sys

try:
    import RPi.GPIO as GPIO
except ImportError:
    print('Missing module: RPi.GPIO\n'
        + 'Defaulting to Mock.GPIO')
    import Mock.GPIO as GPIO
except RuntimeError:
    print('Hardware is not Raspberry Pi\n'
        + 'Defaulting to Mock.GPIO')
    import Mock.GPIO as GPIO

from common.event import Event_
from common.gpio_pin import GPIOPin
from common.singleton import Singleton
from core import gpio_init
from core.gui import GUI
from daemons.gpio_listener import GPIOListener
from daemons.canbus import CANBus
from daemons.logger import Logger
from threading import Event


class Container(metaclass = Singleton):
    def __init__(self, should_stop_with_gui: bool = False):
        print('Initializing KSR')
        
        self._should_stop_with_gui = should_stop_with_gui
        self._should_stop = Event()
        
        print('Initializing GPIO')
        gpio_init.configure_gpio()
        GPIO.output(GPIOPin.KSR_IS_RUNNING.value, GPIO.HIGH)
        
        print('Initializing Daemons')
        
        self.canbus = CANBus()
        self.logger = Logger()
        self.event_listener = GPIOListener()

        self._daemons = [
            self.event_listener,
            self.canbus,
            self.logger
        ]
        
        print('Initializing GUI')
        self._gui = GUI()
        
        print('KSR initialized')
        
    def start(self):
        print('Starting KSR')
    
        print('Starting daemons')
        for d in self._daemons:
            if not d.is_disabled:
                d.start()
                print(d.name + ' started')
            else:
                print(d.name + ' did not start (disabled)')

        print('Starting GUI')
        self._gui.start()
        if self._should_stop_with_gui:
            self.stop()
        else:
            self._should_stop.wait()
        
    def stop(self):
        print('Exiting KSR')
        
        self._should_stop.set()
        self._gui.stop()
        
        print('Stopping daemons')
        for d in reversed(self._daemons):
            if d.is_alive():
                d.stop()
                d.join()
                print(d.name + ' stopped')
        
        GPIO.output(GPIOPin.KSR_IS_RUNNING.value, GPIO.LOW)
        sys.exit(0)
