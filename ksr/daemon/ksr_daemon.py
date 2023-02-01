#!/usr/bin/env python3

"""ksr_daemon.py: Superclass of all KSR deamon threads."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.6"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

#from abc import ABC, abstractmethod
from threading import Event


class KSRDaemon():
    def __init__(self):
        self.is_disabled = False
        self.is_fully_initialized = False
        self._stop_ = Event()
        
    #@abstractmethod
    def stop(self):
        self._stop_.set()