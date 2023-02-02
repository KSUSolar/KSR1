#!/usr/bin/env python3.10

"""ksr_daemon.py: Superclass of all KSR deamon threads."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.6"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

from common.singleton import Singleton
from threading import Event, Thread


class KSRDaemon(Thread, metaclass = Singleton):
    def __new__(cls): # Prevent instantiation without subclass.
        if cls is KSRDaemon:
            raise TypeError('KSRDaemon cannot be instantiated.')
        return object.__new__(cls)
    
    def __init__(self, name: str):
        Thread.__init__(self, name = name, daemon = True)
        self._is_disabled = False
        self._stop_ = Event()
        
    def run(self):
        raise NotImplementedError('Subclasses of KSRDaemon must implement run()') 
    
    def stop(self):
        self._stop_.set()
        
    def disable(self):
        self._is_disabled = True
        
    @property
    def is_disabled(self):
        return self._is_disabled