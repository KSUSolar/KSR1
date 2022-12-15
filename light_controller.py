import RPi.GPIO as GPIO
import time

from threading import Thread


class LightController(Thread):
    def __init__(self):
        Thread.__init__(self)
        self._running = True
        self._l_blinker_on = False
        self._r_blinker_on = False

    def run(self):
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

        while self._running:
            if GPIO.input(L_BLINKER_INPUT_PIN) == 1:
                GPIO.output(L_BLINKER_OUTPUT_PIN, GPIO.HIGH)
                self._l_blinker_on = True
                time.sleep(0.5)

                GPIO.output(L_BLINKER_OUTPUT_PIN, GPIO.LOW)
                self._l_blinker_on = False
                time.sleep(0.5)

            elif GPIO.input(R_BLINKER_INPUT_PIN) == 1:
                GPIO.output(R_BLINKER_OUTPUT_PIN, GPIO.HIGH)
                self._r_blinker_on = True
                time.sleep(0.5)

                GPIO.output(R_BLINKER_OUTPUT_PIN, GPIO.LOW)
                self._r_blinker_on = False
                time.sleep(0.5)

            elif GPIO.input(HAZ_INPUT_PIN) == 1:
                GPIO.output(R_BLINKER_OUTPUT_PIN, GPIO.HIGH)
                GPIO.output(L_BLINKER_OUTPUT_PIN, GPIO.HIGH)
                self._l_blinker_on = True
                self._r_blinker_on = True
                time.sleep(0.5)

                GPIO.output(R_BLINKER_OUTPUT_PIN, GPIO.LOW)
                GPIO.output(L_BLINKER_OUTPUT_PIN, GPIO.LOW)
                self._l_blinker_on = False
                self._r_blinker_on = False
                time.sleep(0.5)

            else:
                time.sleep(0.016)

    def stop(self):
        self._running = False

    @property
    def l_blinker_on(self):
        return self._l_blinker_on

    @property
    def r_blinker_on(self):
        return self._r_blinker_on