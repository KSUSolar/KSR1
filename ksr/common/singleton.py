#!/usr/bin/env python3

"""singleton.py: Singleton metaclass. Thread safe"""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.6"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"


from threading import Lock
from typing import Any, Dict


class Singleton(type):
    _instances = {}
    _locks: Dict[Any, Lock()] = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances: # Check lock is needed.
            if cls not in cls._locks: # Prevent deadlock.
                cls._locks[cls] = Lock()
            with cls._locks[cls]:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]