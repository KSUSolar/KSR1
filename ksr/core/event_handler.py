#!/usr/bin/env python3.10

"""main.py: Handles queued KSR events."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.6"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import threading

from common.event import Event_
from core.gui_dep import GUI
from concurrent.futures import ThreadPoolExecutor

_event_executor = ThreadPoolExecutor(max_workers = 8)

def bind(event: Event_):
    #if not threading.current_thread().name.startswith('Thread-'):
    #    _event_executor.submit(bind, event)
    #    return
    
    from core.container import Container
    container = Container()
    
    match event:
        case Event_.L_BLINKER_ON:
            return
        case Event_.L_BLINKER_OFF:
            return
        case Event_.R_BLINKER_ON:
            return
        case Event_.R_BLINKER_OFF:
            return
        case Event_.HAZ_ON:
            return
        case Event_.HAZ_OFF:
            return
        
        case Event_.KSR_SHUTDOWN:
            container.stop()
        case Event_.GUI_CLOSE:
            print('GUI closed')
            bind(Event_.KSR_SHUTDOWN)
        case Event_.HARDWARE_SHUTDOWN:
            #gui = GUI(None)
            #gui.close()
            return
            
        case Event_.CANBUS_INTR:
            print('Warning: CANBus daemon interrupt')
            # TODO: Add GUI canbus warning.
            return
        case Event_.TRANSMITTER_INTR:
            # TODO: Add GUI transmitter warning.
            return