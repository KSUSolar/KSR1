#!/usr/bin/env python3

"""ksr.py: Main entrypoint for KSR program."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.7"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import platform
import sys

from core.container import Container

sys.path.append('ksr') # Add ksr directory to path

if __name__ == '__main__':
    operating_system = platform.system() 
    if operating_system != "Linux": # Check that KSR is running on Linux.
        print('KSR cannot be run on: ' + operating_system 
            + "\nExiting KSR")
        sys.exit(1)
        
    container = Container(should_stop_with_gui=True)
    container.start()