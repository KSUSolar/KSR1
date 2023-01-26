#!/usr/bin/env python3

"""logger.py: Dumps canbus.py data to M/D/Y_H:M:S.csv"""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.3"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import csv
import numpy as np
import time

from canbus import CanBus
from datetime import datetime
from threading import Thread


class Logger(Thread):
    def __init__(self, canbus: CanBus):
        Thread.__init__(self)
        self._canbus = canbus
        self._running = True

    def run(self):
        current_date = datetime.now().strftime('%y-%m-%d')
        start_time = self.__current_time_hms()[:-3]
        log_dir = 'logs/' + current_date + '_' + start_time + '.csv'

        with open(log_dir, 'w') as log:
            writer = csv.writer(log)
            
        writer.writerow(self._canbus.stats.keys()) # Canbus headers.
        while self._running:
            writer.writerow(self.__current_time_hms() + self._canbus.stats.values())
            time.sleep(0.5)

        log.close()

    def stop(self):
        self._running = False

    @staticmethod
    def __current_time_hms():
        current_time = datetime.now()
        return current_time.strftime('%H:%M:%S') + '.' + current_time.microsecond / 1000    