#!/usr/bin/env python3.10

"""event.py: KSR events."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.6"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

from enum import Enum, auto


class Event_(Enum):
    GUI_CLOSE = auto() # GUI closed.
    KSR_SHUTDOWN = auto() # KSR shutdown condition met.
    
    CANBUS_INTR = auto() # CANBus daemon interrupted.
    TRANSMITTER_INTR = auto() # Transmitter daemon interrupted.
    
    L_BLINKER_ON = auto() # Condition for left blinker on met.
    L_BLINKER_OFF = auto() # Condition for left blinker off met.
    R_BLINKER_ON = auto() # Condition for right blinker on met.
    R_BLINKER_OFF = auto() # Condition for right blinker off met.
    HAZ_ON = auto() # Condition for hazard on met.
    HAZ_OFF = auto() # Condition for hazard off met.
    
    HARDWARE_SHUTDOWN = auto() # Shutdown button pressed.