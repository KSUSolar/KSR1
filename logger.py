#!/usr/bin/env python3

"""logger.py: Dumps canbus.py data to M/D/Y_H:M:S.csv"""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.4"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import csv
import pi_tel as pi

from canbus import CANBus
from datetime import datetime
from threading import Event, Thread


class Logger(Thread):
    THREAD_NAME = 'Logger'

    def __init__(self, canbus: CANBus):
        Thread.__init__(self, name = self.THREAD_NAME)
        self._canbus = canbus
        self._stop = Event()

    def run(self):
        print(self.name + ' started')

        date = pi.current_date_ymd()
        start_time = pi.current_time_hms()#[:-3]
        log_dir = 'logs/' + date + '_' + start_time + '.csv'

        with open(log_dir, 'w') as log:
            writer = csv.writer(log)
            writer.writerow(['Timestamp', 'Pi Temp'] + self._canbus.data.keys()) # Canbus headers.
            while not self._stop.is_set():
                writer.writerow([self.__current_time_hms(), pi.temp()] + list(self._canbus.stats.values()))
                self._stop.wait(1)
            log.close()

    def stop(self):
        print('Shutting down ' + self.name)
        self._stop.set()