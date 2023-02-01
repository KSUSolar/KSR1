#!/usr/bin/env python3

"""event_listener.py: Listens for GPIO & daemon state changes."""

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
    import Mock.GPIO as GPIO # Dev.

from common.event import Event_
from common.gpio_pin import GPIOPin
from common.singleton import Singleton
from core import event_handler
from core.light_controller import LightController
from core.gui_dep import GUI
from daemon.canbus import CANBus
from daemon.ksr_daemon import KSRDaemon
from threading import Thread


class EventListener(Thread, KSRDaemon, metaclass = Singleton):
    _THREAD_NAME = 'EventListener'
    
    def __init__(self):
        Thread.__init__(self, name = self._THREAD_NAME, daemon = True)
        KSRDaemon.__init__(self)
    
    def run(self):
        #canbus = CANBus()
        
        while not self._stop_.is_set():
            if GPIO.input(GPIOPin.HAZ_INPUT) == 1:
                if LightController.l_blinker_on:
                    event_handler.bind(Event_.L_BLINKER_OFF)
                if LightController.r_blinker_on:
                    event_handler.bind(Event_.R_BLINKER_OFF)
                event_handler.bind(Event_.HAZ_ON)
            elif LightController.haz_on:
                event_handler.bind(Event_.HAZ_OFF)
            if GPIO.input(GPIOPin.L_BLINKER_INPUT) == 1 and not LightController.haz_on:
                event_handler.bind(Event_.L_BLINKER_ON)
            elif LightController.l_blinker_on:
                event_handler.bind(Event_.L_BLINKER_OFF)
            if GPIO.input(GPIOPin.R_BLINKER_INPUT) == 1 and not LightController.haz_on:
                event_handler.bind(Event_.R_BLINKER_ON)
            elif LightController.r_blinker_on:
                event_handler.bind(Event_.R_BLINKER_OFF)
                
            if GPIO.input(GPIOPin.SHUTDOWN) == 1:
                event_handler.bind(Event_.HARDWARE_SHUTDOWN)
                
            #if self._gui.is_closed:
            #    event_handler.bind(Event_.GUI_CLOSE)
                
            #if not self._canbus.is_alive():
            #    event_handler.bind(Event_.CANBUS_INTR)
                
            # Implement Transmitter check.