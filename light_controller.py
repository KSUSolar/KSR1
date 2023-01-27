#!/usr/bin/env python3

"""light_controller.py: Uses GPIO to control car blinkers."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.4"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import RPi.GPIO as GPIO

from threading import Event, Thread


class LightController(Thread):
    THREAD_NAME = 'LightController'

    def __init__(self):
        Thread.__init__(self, name = self.THREAD_NAME)
        self._stop = Event()
        self._l_blinker_on = False
        self._r_blinker_on = False

    def run(self):
        print(self.name + ' started')

        L_BLINKER_OUTPUT_PIN = 6
        R_BLINKER_OUTPUT_PIN = 5
        L_BLINKER_INPUT_PIN = 27
        R_BLINKER_INPUT_PIN = 17
        HAZ_INPUT_PIN = 22

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(L_BLINKER_OUTPUT_PIN, GPIO.OUT)
        GPIO.setup(R_BLINKER_OUTPUT_PIN, GPIO.OUT)
        GPIO.output(L_BLINKER_OUTPUT_PIN, 0)
        GPIO.output(R_BLINKER_OUTPUT_PIN, 0)

        GPIO.setup(L_BLINKER_INPUT_PIN , GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(R_BLINKER_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(HAZ_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        while not self._stop.is_set():
            if GPIO.input(L_BLINKER_INPUT_PIN) == 1:
                GPIO.output(L_BLINKER_OUTPUT_PIN, GPIO.HIGH)
                self._l_blinker_on = True
                self._stop.wait(0.5)

                GPIO.output(L_BLINKER_OUTPUT_PIN, GPIO.LOW)
                self._l_blinker_on = False
                self._stop.wait(0.5)

            elif GPIO.input(R_BLINKER_INPUT_PIN) == 1:
                GPIO.output(R_BLINKER_OUTPUT_PIN, GPIO.HIGH)
                self._r_blinker_on = True
                self._stop.wait(0.5)

                GPIO.output(R_BLINKER_OUTPUT_PIN, GPIO.LOW)
                self._r_blinker_on = False
                self._stop.wait(0.5)

            elif GPIO.input(HAZ_INPUT_PIN) == 1:
                GPIO.output(R_BLINKER_OUTPUT_PIN, GPIO.HIGH)
                GPIO.output(L_BLINKER_OUTPUT_PIN, GPIO.HIGH)
                self._l_blinker_on = True
                self._r_blinker_on = True
                self._stop.wait(0.5)

                GPIO.output(R_BLINKER_OUTPUT_PIN, GPIO.LOW)
                GPIO.output(L_BLINKER_OUTPUT_PIN, GPIO.LOW)
                self._l_blinker_on = False
                self._r_blinker_on = False
                self._stop.wait(0.5)

    def stop(self):
        print('Shutting down ' + self.name)
        self._stop.set()

    @property
    def l_blinker_on(self):
        return self._l_blinker_on

    @property
    def r_blinker_on(self):
        return self._r_blinker_on