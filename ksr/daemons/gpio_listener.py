#!/usr/bin/env python3

"""gpio_listener.py: Listens for GPIO state changes."""

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
except RuntimeError:
    print('Hardware is not Raspberry Pi\n'
        + 'Defaulting to Mock.GPIO')
    import Mock.GPIO as GPIO

from common.event import Event_
from common.gpio_pin import GPIOPin
from core import event_handler
from core.light_controller import LightController
from daemons.ksr_daemon import KSRDaemon


class GPIOListener(KSRDaemon):
    _THREAD_NAME = 'GPIOListener'
    
    def __init__(self):
        KSRDaemon.__init__(self, self._THREAD_NAME)
    
    def run(self):
        while not self._stop_.is_set():
            if GPIO.input(GPIOPin.HAZ_INPUT) == 1:
                if LightController.is_l_blinker_on() or LightController.is_r_blinker_on():
                    event_handler.bind(Event_.BLINKERS_OFF)
                event_handler.bind_async(Event_.HAZ_ON)
            elif LightController.is_haz_on():
                event_handler.bind(Event_.BLINKERS_OFF)
                
            if GPIO.input(GPIOPin.L_BLINKER_INPUT) == 1 and not LightController.haz_on:
                event_handler.bind_asnyc(Event_.L_BLINKER_ON)
            elif LightController.is_l_blinker_on():
                event_handler.bind(Event_.BLINKERS_OFF)
                
            if GPIO.input(GPIOPin.R_BLINKER_INPUT) == 1 and not LightController.haz_on:
                event_handler.bind_async(Event_.R_BLINKER_ON)
            elif LightController.is_r_blinker_on():
                event_handler.bind(Event_.BLINKERS_OFF)
                
            if GPIO.input(GPIOPin.SHUTDOWN) == 1:
                event_handler.bind_async(Event_.HARDWARE_SHUTDOWN)
                
            self._stop_.wait(1 / 60)