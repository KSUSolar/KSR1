#!/usr/bin/env python3

"""light_controller.py: Uses GPIO to control car blinkers."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.5"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import RPi.GPIO as GPIO
#import Mock.GPIO as GPIO # Dev.

from threading import Event, Thread


class LightController(Thread):
    THREAD_NAME = 'LightController'
    
    L_BLINKER_OUTPUT_PIN = 6
    R_BLINKER_OUTPUT_PIN = 5
    L_BLINKER_INPUT_PIN = 27
    R_BLINKER_INPUT_PIN = 17
    HAZ_INPUT_PIN = 22

    def __init__(self, stop_: Event):
        Thread.__init__(self, name = self.THREAD_NAME, daemon = True)
        self._stop_ = stop_
        self._l_blinker_on = False
        self._r_blinker_on = False
        
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.L_BLINKER_OUTPUT_PIN, GPIO.OUT)
        GPIO.setup(self.R_BLINKER_OUTPUT_PIN, GPIO.OUT)
        GPIO.output(self.L_BLINKER_OUTPUT_PIN, 0)
        GPIO.output(self.R_BLINKER_OUTPUT_PIN, 0)

        GPIO.setup(self.L_BLINKER_INPUT_PIN , GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.R_BLINKER_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.HAZ_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def run(self):
        while not self._stop_.is_set():
            if GPIO.input(self.L_BLINKER_INPUT_PIN) == 1:
                GPIO.output(self.L_BLINKER_OUTPUT_PIN, GPIO.HIGH)
                self._l_blinker_on = True
                self._stop_.wait(0.5)

                GPIO.output(self.L_BLINKER_OUTPUT_PIN, GPIO.LOW)
                self._l_blinker_on = False
                self._stop_.wait(0.5)

            elif GPIO.input(self.R_BLINKER_INPUT_PIN) == 1:
                GPIO.output(self.R_BLINKER_OUTPUT_PIN, GPIO.HIGH)
                self._r_blinker_on = True
                self._stop_.wait(0.5)

                GPIO.output(self.R_BLINKER_OUTPUT_PIN, GPIO.LOW)
                self._r_blinker_on = False
                self._stop_.wait(0.5)

            elif GPIO.input(self.HAZ_INPUT_PIN) == 1:
                GPIO.output(self.R_BLINKER_OUTPUT_PIN, GPIO.HIGH)
                GPIO.output(self.L_BLINKER_OUTPUT_PIN, GPIO.HIGH)
                self._l_blinker_on = True
                self._r_blinker_on = True
                self._stop_.wait(0.5)

                GPIO.output(self.R_BLINKER_OUTPUT_PIN, GPIO.LOW)
                GPIO.output(self.L_BLINKER_OUTPUT_PIN, GPIO.LOW)
                self._l_blinker_on = False
                self._r_blinker_on = False
                self._stop_.wait(0.5)

    @property
    def l_blinker_on(self):
        return self._l_blinker_on

    @property
    def r_blinker_on(self):
        return self._r_blinker_on