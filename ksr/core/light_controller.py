#!/usr/bin/env python3

"""light_controller.py: Uses GPIO to control car blinkers."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.7"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

try:
    import RPi.GPIO as GPIO
except ImportError and RuntimeError:
    import Mock.GPIO as GPIO # Dev.
    
from common.gpio_pin import GPIOPin
from threading import Event, Lock


class LightController:
    _should_stop = Event()
    _lock = Lock()
    _is_l_blinker_on = False
    _is_l_blinker_light_on = False
    _is_r_blinker_on = False
    _is_r_blinker_light_on = False
    _is_haz_on = False

    def __init__(self):
        raise TypeError('LightController cannot be instantiated.')

    @classmethod
    def blink_left(cli):
        cli.is_l_blinker_on = True
        
        while not cli._should_stop.is_set():
            GPIO.output(GPIOPin.L_BLINKER_OUTPUT, GPIO.HIGH)
            cli._set_l_blinker(True)
            cli._should_stop.wait(0.5)

            GPIO.output(GPIOPin.L_BLINKER_OUTPUT, GPIO.LOW)
            cli._set_l_blinker(False)
            cli._should_stop.wait(0.5)
            
        cli.is_l_blinker_on = False

    @classmethod
    def blink_right(cli):
        cli.is_r_blinker_on = True
        
        while not cli._should_stop.is_set():
            GPIO.output(GPIOPin.R_BLINKER_OUTPUT, GPIO.HIGH)
            cli._set_r_blinker(True)
            cli._should_stop.wait(0.5)

            GPIO.output(GPIOPin.R_BLINKER_OUTPUT, GPIO.LOW)
            cli._set_r_blinker(False)
            cli._should_stop.wait(0.5)
        
        cli.is_r_blinker_on = False

    @classmethod
    def blink_haz(cli):
        cli.is_haz_on = True
        
        while not cli._should_stop.is_set():
            GPIO.output(GPIOPin.L_BLINKER_OUTPUT, GPIO.HIGH)
            GPIO.output(GPIOPin.R_BLINKER_OUTPUT, GPIO.HIGH)
            cli._set_l_blinker(True)
            cli._set_r_blinker(True)
            cli._should_stop.wait(0.5)

            GPIO.output(GPIOPin.L_BLINKER_OUTPUT, GPIO.LOW)
            GPIO.output(GPIOPin.R_BLINKER_OUTPUT, GPIO.LOW)
            cli._set_l_blinker(False)
            cli._set_r_blinker(False)
            cli._should_stop.wait(0.5)
        
        cli.is_haz_on = False
        
    @classmethod
    def stop_blinkers(cli):
        cli._should_stop.set()
        
    @classmethod
    def is_l_blinker_on(cli):
        return cli._is_l_blinker_on
    
    @classmethod
    def _set_l_blinker(cli, value: bool):
        with cli._lock:
            cli._is_l_blinker_on = value
            
    @classmethod
    def is_l_blinker_light_on(cli):
        return cli._is_l_blinker_light_on
    
    @classmethod
    def is_r_blinker_on(cli):
        return cli._is_r_blinker_on
    
    @classmethod
    def _set_r_blinker(cli, value: bool):
        with cli._lock:
            cli._is_r_blinker_on = value
            
    @classmethod
    def is_r_blinker_light_on(cli):
        return cli._is_r_blinker_light_on
            
    @classmethod
    def is_haz_on(cli):
        return cli._is_haz_on
    
    @classmethod
    def _set_haz(cli, value: bool):
        with cli._lock:
            cli._is_haz_on = value