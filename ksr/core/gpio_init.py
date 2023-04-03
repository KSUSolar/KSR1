"""gpio_init.py: Configures GPIO."""

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

from common.gpio_pin import GPIOPin


def configure_gpio() -> None:
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(GPIOPin.SHUTDOWN.value, GPIO.IN)
    GPIO.setup(GPIOPin.L_BLINKER_INPUT.value, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(GPIOPin.R_BLINKER_INPUT.value, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(GPIOPin.HAZ_INPUT.value, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    GPIO.setup(GPIOPin.KSR_IS_RUNNING.value, GPIO.OUT)
    GPIO.output(GPIOPin.KSR_IS_RUNNING.value, 0)
    GPIO.setup(GPIOPin.CANBUS_IS_RUNNING.value, GPIO.OUT)
    GPIO.output(GPIOPin.CANBUS_IS_RUNNING.value, 0)
    GPIO.setup(GPIOPin.LOGGER_IS_RUNNING.value, GPIO.OUT)
    GPIO.output(GPIOPin.LOGGER_IS_RUNNING.value, 0)
    GPIO.setup(GPIOPin.L_BLINKER_OUTPUT.value, GPIO.OUT)
    GPIO.output(GPIOPin.L_BLINKER_OUTPUT.value, 0)
    GPIO.setup(GPIOPin.R_BLINKER_OUTPUT.value, GPIO.OUT)
    GPIO.output(GPIOPin.R_BLINKER_OUTPUT.value, 0)
