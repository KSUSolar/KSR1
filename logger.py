#!/usr/bin/env python3

"""logger.py: Dumps canbus.py data to M/D/Y_H:M:S.csv"""

__author__      = "Daniel Tebor"
__copyright__   = ""
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.3"
__maintainer__  = ""
__email__       = ""
__status__      = "Development"

from datetime import datetime
from threading import Thread


class Logger(Thread):
    def __init__(self):
        Thread.__init__(self)

    #def run(self):