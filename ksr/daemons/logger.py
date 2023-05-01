#!/usr/bin/env python3

"""logger.py: Logs canbus.py & pi telemetry data to M/D/Y_H:M:S.csv"""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.7"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import csv
import os
import common.pi_tm as pi

try:
    import RPi.GPIO as GPIO
except ImportError:
    print('Missing module: RPi.GPIO\n'
        + 'Defaulting to Mock.GPIO')
    import Mock.GPIO as GPIO
except RuntimeError:
    print('Hardware is not Raspberry Pi\n'
        + 'Defaulting to Mock.GPIO')
    import Mock.GPIO as GPIO

from common.gpio_pin import GPIOPin
from daemons.canbus import CANBus
from daemons.ksr_daemon import KSRDaemon


class Logger(KSRDaemon):
    _THREAD_NAME = 'Logger'
    _SAVE_INTRV_MINS = 1 # Approximately accurate. #I'll change this back to 5 after testing

    def __init__(self):
        KSRDaemon.__init__(self, self._THREAD_NAME)

        self._canbus = CANBus()
        
        # Disable if CANBus is disabled.
        if self._canbus.is_disabled:
            print(self.name + ' daemon disabled: ' 
                + self.name + ' dependent on ' + self._canbus.name + ' daemon')
            self.disable()
            
        self._is_initialized = True

    def run(self):
        if self.is_disabled:
            print(self.name + ' disabled. Stopping')
            return
        
        GPIO.output(GPIOPin.LOGGER_IS_RUNNING.value, GPIO.HIGH)
        
        date = pi.current_date_ymd()
        start_time = pi.current_time_hms()#[:-3]
        log_name = date + '_' + start_time + '.csv'
        log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs', log_name)
        
        with open(log_dir, 'w') as log:
            writer = csv.writer(log)
            writer.writerow(['Timestamp', 'Pi Temp']
                + list(self._canbus.data.keys())) # Canbus headers.
            log.close()

        # Write new line to csv every second. Save csv ~ every SAVE_INTRV_MINS mins.
        # Save and break loop if CANBus deamon is interrupted.
        while not self._should_stop.is_set():
            num_seconds = 1

            with open(log_dir, 'a') as log:
                writer = csv.writer(log)
                
                while num_seconds < self._SAVE_INTRV_MINS * 60 and not self._should_stop.is_set():
                    if not self._canbus.is_alive():
                        writer.writerow([self._canbus.name + ' daemon interrupt'])
                        self._should_stop.set()
                        break
                    
                    writer.writerow([pi.current_time_hms(), pi.temp()]
                        + list(self._canbus.data.values()))
                    
                    num_seconds += 1
                    self._should_stop.wait(1)
                    
                log.close()
                
        GPIO.output(GPIOPin.LOGGER_IS_RUNNING.value, GPIO.LOW)
