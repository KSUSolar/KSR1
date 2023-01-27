#!/usr/bin/env python3

"""pi_tel.py: Raspberry pi telemetry functions."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.4"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import datetime

from gpiozero import CPUTemperature

def temp():
    return CPUTemperature.temperature

def current_date_ymd():
    return datetime.now().strftime('%y-%m-%d')

def current_time_hms():
    current_time = datetime.now()
    return current_time.strftime('%H:%M:%S')# + '.' + str(current_time.microsecond)[:-4]