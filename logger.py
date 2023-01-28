#!/usr/bin/env python3

"""logger.py: Dumps canbus.py data to M/D/Y_H:M:S.csv"""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.5"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import csv
import pi_tm as pi

from canbus import CANBus
from threading import Event, Thread


class Logger(Thread):
    THREAD_NAME = 'Logger'
    SAVE_INTRV_MINS = 5 # Approximately accurate.

    def __init__(self, stop_: Event, canbus: CANBus):
        Thread.__init__(self, name = self.THREAD_NAME, daemon = True)
        self._stop_ = stop_
        self._canbus = canbus

    def run(self):
        date = pi.current_date_ymd()
        start_time = pi.current_time_hms()#[:-3]
        log_dir = 'logs/' + date + '_' + start_time + '.csv'

        with open(log_dir, 'w') as log:
            writer = csv.writer(log)
            writer.writerow(['Timestamp', 'Pi Temp']
                + list(self._canbus.data.keys())) # Canbus headers.
            log.close()

        # Write new line to csv every second. Save csv ~ every SAVE_INTRV_MINS mins.
        # Save and break loop if CANBus deamon is interrupted.
        while not self._stop_.is_set():
            num_seconds = 1

            with open(log_dir, 'a') as log:
                writer = csv.writer(log)
                
                while num_seconds < self.SAVE_INTRV_MINS * 60 and not self._stop_.is_set():
                    if not self._canbus.is_alive():
                        writer.writerow([self._canbus.name + ' daemon interrupt'])
                        break
                    
                    writer.writerow([pi.current_time_hms(), pi.temp()]
                        + list(self._canbus.data.values()))
                    
                    num_seconds += 1
                    self._stop_.wait(1)
                    
                log.close()
                
            if not self._canbus.is_alive():
                break