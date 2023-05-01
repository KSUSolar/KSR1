#!/usr/bin/env python3

"""gpio_pin.py: Values for used GPIO pins."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.7"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

from enum import Enum


class GPIOPin(Enum):
    SHUTDOWN = 2
    KSR_IS_RUNNING = 16
    CANBUS_IS_RUNNING = 23
    LOGGER_IS_RUNNING = 24
    
    L_BLINKER_INPUT = 27
    L_BLINKER_OUTPUT = 6
    R_BLINKER_INPUT = 17
    R_BLINKER_OUTPUT = 5
    HAZ_INPUT = 22