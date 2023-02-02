#!/usr/bin/env python3.10

"""light_controller.py: Uses GPIO to control car blinkers."""

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
except ImportError and RuntimeError:
    import Mock.GPIO as GPIO # Dev.
    
from common.gpio_pin import GPIOPin
from threading import Event


class LightController:
    l_blinker_on = False
    l_blinker_light_on = False
    r_blinker_on = False
    r_blinker_light_on = False
    haz_on = False

    def __init__(self):
        raise TypeError("Cannot make instances of 'LightController'")

    @classmethod
    def blink_left(cli, stop: Event):
        cli.l_blinker_on = True
        
        while not stop.is_set():
            GPIO.output(GPIOPin.L_BLINKER_OUTPUT, GPIO.HIGH)
            cli.l_blinker_light_on = True
            stop.wait(0.5)

            GPIO.output(GPIOPin.L_BLINKER_OUTPUT, GPIO.LOW)
            cli.l_blinker_light_on = False
            stop.wait(0.5)
            
        cli.l_blinker_light_on = False
        cli.l_blinker_on = False

    @classmethod
    def blink_right(cli, stop: Event):
        cli.r_blinker_on = True
        
        while not stop.is_set():
            GPIO.output(GPIOPin.R_BLINKER_OUTPUT, GPIO.HIGH)
            cli.r_blinker_light_on = True
            stop.wait(0.5)

            GPIO.output(GPIOPin.R_BLINKER_OUTPUT, GPIO.LOW)
            cli.l_blinker_light_on = False
            stop.wait(0.5)
        
        cli.l_blinker_light_on = False
        cli.l_blinker_on = False

    @classmethod
    def blink_haz(cli, stop: Event):
        cli.haz_on = True
        
        while not stop.is_set():
            GPIO.output(GPIOPin.L_BLINKER_OUTPUT, GPIO.HIGH)
            GPIO.output(GPIOPin.R_BLINKER_OUTPUT, GPIO.HIGH)
            cli.l_blinker_light_on = True
            cli.r_blinker_light_on = True
            stop.wait(0.5)

            GPIO.output(GPIOPin.L_BLINKER_OUTPUT, GPIO.LOW)
            GPIO.output(GPIOPin.R_BLINKER_OUTPUT, GPIO.LOW)
            cli.l_blinker_light_on = False
            cli.r_blinker_light_on = False
            stop.wait(0.5)
        
        cli.l_blinker_light_on = False
        cli.r_blinker_light_on = False
        cli.haz_on = False