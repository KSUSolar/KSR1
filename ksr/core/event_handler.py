#!/usr/bin/env python3

"""main.py: Handles queued KSR events."""

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
from concurrent.futures import ThreadPoolExecutor

from core.light_controller import LightController

_event_executor = ThreadPoolExecutor(max_workers = 8)

def bind(event: Event_):
    from core.container import Container
    container = Container()
    
    if event == Event_.BLINKERS_OFF:
        LightController.stop_blinkers()
    elif event == Event_.L_BLINKER_ON:
        LightController.blink_left()
    elif event == Event_.R_BLINKER_ON:
        LightController.blink_right()
    elif event == Event_.HAZ_ON:
        LightController.blink_haz()
    
    elif event == Event_.KSR_SHUTDOWN:
        container.stop()
    elif event == Event_.GUI_CLOSE:
        print('GUI closed')
        bind(Event_.KSR_SHUTDOWN)
    elif event == Event_.HARDWARE_SHUTDOWN:
        #gui = GUI(None)
        #gui.close()
        bind(Event_.KSR_SHUTDOWN)
        
    elif event == Event_.CANBUS_INTR:
        GPIO.output(GPIOPin.CANBUS_IS_RUNNING.value, GPIO.LOW)
        print('Warning: CANBus daemon interrupt')
        # TODO: Add GUI canbus warning.
        return
    elif event == Event_.TRANSMITTER_INTR:
        # TODO: Add GUI transmitter warning.
        return
    
def bind_async(event: Event_):
    _event_executor.submit(bind, event)
