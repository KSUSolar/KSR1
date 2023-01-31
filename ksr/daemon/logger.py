#!/usr/bin/env python3

"""logger.py: Logs canbus.py & pi telemetry data to M/D/Y_H:M:S.csv"""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.6"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import csv
import os
import time
import common.pi_tm as pi

from daemon.canbus import CANBus
from daemon.ksr_daemon import KSRDaemon
from threading import Thread


class Logger(Thread, KSRDaemon):
    THREAD_NAME = 'Logger'
    SAVE_INTRV_MINS = 5 # Approximately accurate.

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.__init__(*args, **kwargs)
        return cls._instance

    def __init__(self, canbus: CANBus):
        Thread.__init__(self, name = self.THREAD_NAME, daemon = True)
        KSRDaemon.__init__(self, self.THREAD_NAME)
        self._canbus = canbus

    def run(self):
        date = pi.current_date_ymd()
        start_time = pi.current_time_hms()#[:-3]
        log_name = date + '_' + start_time + '.csv'
        log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs', log_name)

        with open(log_dir, 'w') as log:
            writer = csv.writer(log)
            writer.writerow(['Timestamp', 'Pi Temp']
                + list(self._canbus.data.keys())) # Canbus headers.
            log.close()
        time.sleep(1)

        # Write new line to csv every second. Save csv ~ every SAVE_INTRV_MINS mins.
        # Save and break loop if CANBus deamon is interrupted.
        while not self._stop_.is_set():
            num_seconds = 1

            with open(log_dir, 'a') as log:
                writer = csv.writer(log)
                
                while num_seconds < self.SAVE_INTRV_MINS * 60 and not self._stop_.is_set():
                    if not self._canbus.is_alive():
                        writer.writerow([self._canbus.name + ' daemon interrupt'])
                        self._stop_.set()
                        break
                    
                    writer.writerow([pi.current_time_hms(), pi.temp()]
                        + list(self._canbus.data.values()))
                    
                    num_seconds += 1
                    self._stop_.wait(1)
                    
                log.close()