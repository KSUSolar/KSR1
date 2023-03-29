#!/usr/bin/env python3

"""canbus.py: Retrieves hardware telemetry using the 'can0' network interface."""

__author__      = "Aaron Harbin, Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.6"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

import can
import os

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

from daemons.ksr_daemon import KSRDaemon
from common.event import Event_
from common.gpio_pin import GPIOPin
from core import event_handler


class CANBus(KSRDaemon):
    _THREAD_NAME = 'CANBus'

    # Timeout if the canbus is unresponsive.
    _RECV_TIMEOUT = 10

    # Motor controller packets for motor and motor controller.
    _MOTOR_DATA_ID1 = 217128575
    _MOTOR_DATA_ID2 = 217128831

    # BMS data packets for battery.
    _BATT_DATA_ID1 = 1712
    _BATT_DATA_ID2 = 1713

    # MPPT packets for solar array.
    # TODO: Determine IDs
    _SOLAR_DATA_ID1 = 404 # Don't know
    _SOLAR_DATA_ID2 = 404 # Don't know
    _SOLAR_DATA_ID3 = 404 # Don't know

    _ERROR_CODES = [
        "0:Identification",
        "1:Over Volt",
        "2:Low Volt",
        "3:Reserved",
        "4:Stall",
        "5:InteralVolt",
        "6:Contr.OVERTEMP",
        "7:THR_ON_PWR",
        "8:Reserved2",
        "9:InternalReset",
        "10:Hall-Open/Short",
        "11:AngleSensor",
        "12:Reserve3",
        "13:Reserve4",
        "14:MotorOVERTEMP",
        "15:Pi_Code_Error"
    ]

    def __init__(self):
        KSRDaemon.__init__(self, self._THREAD_NAME)
        
        self._gear = 1

        self._mph = 0
        self._kelly_motor_temp = -1
        self._kelly_controller_temp = -1
        self._error_code_readout = ""

        self._batt_temp_avg = -1 # Avg of Battery cell temps.
        self._batt_temp_high = -1 # Temp of hottest cell.
        self._batt_temp_low = -1 # Temp of coolest cell.
        self._batt_temp_high_id = -1  # ID of thermistor measuring hottest cell.
        self._batt_temp_low_id = -1  # ID of thermistor measuring coolest cell.
        self._bpsfault = False

        self._batt_charge_perc = -1
        self._batt_volts = -1
        self._batt_amps = -1
        self._aux_volts = -1

        self._solar_pcb_temp = -1
        self._solar_mosfet_temp = -1
        self._solar_amps_in = -1
        self._solar_volts_in = -1
        self._solar_volts_out = -1
        
        os.system('sudo ip link set can0 type can bitrate 250000') # Create canbus network interface.
        #os.system('sudo ip link set can0 type vcan bitrate 500000') # Dev.
        os.system('sudo ip link set up can0') # Sart canbus network interface.
        
        #TODO: Fix this to work with python-can 4.1.0
        try:
            self._canbus_intf = can.interface.Bus(interface = 'socketcan', 
                                            channel = 'can0', 
                                            baudrate = 250000)
        except OSError as err:
            print('Unable to initialize canbus interface: ' + err.strerror
                + '\n' + self.name + ' daemon disabled')
            self.disable()

    def run(self):
        try:
            if self.is_disabled:
                print(self.name + ' disabled. Stopping')
                return
            
            GPIO.output(GPIOPin.CANBUS_IS_RUNNING, GPIO.HIGH)
            
            while not self._stop_.is_set():
                packets_found = 0
                
                # TODO: Fix way message is read in to work with python-can 4.1.0
                while packets_found < 7 and not self._stop_.is_set():
                    msg = self._canbus_intf.recv(self._RECV_TIMEOUT)
                    if (msg.arbitration_id == self._MOTOR_DATA_ID1):
                        packets_found += 1
                        
                        # This packet gives MPH and error codes.
                        # More info needed from mechanical for accurate MPH.
                        motor_rpm = ((msg[1] * 256) + msg.data[0]) / 10

                        # 14 teeth on motor sprocket.
                        # 47 teeth on swing arm sprocket.
                        # = 0.3617 ratio.
                        wheel_rpm = motor_rpm * 0.3617

                        # RPM to Linear Velocity formula
                        # v = r × RPM × 0.10472
                        self._mph = 0.3048 * wheel_rpm * 0.10472

                        # Reset error codes.
                        self._error_code_readout = ""

                        # Error codes 1
                        error_code1 = bin(msg.data[6])[2:].zfill(8)
                        i = 7
                        while i >= 0:
                            if (error_code1[i] == "1"):
                                self._error_code_readout += self._ERROR_CODES[(i-7)*-1] + ", "
                            i -= 1
                        
                        # Error codes 2
                        i = 7
                        error_code2 = bin(msg.data[7])[2:].zfill(8)
                        while i >= 0:
                            if (error_code2[i] == "1"):
                                self._error_code_readout += self._ERROR_CODES[(i-15)*-1] + ", "
                            i -= 1
                        
                        self._error_code_readout = self._error_code_readout[0:-2]

                    elif (msg.arbitration_id == self._MOTOR_DATA_ID2):
                        packets_found += 1
                        # TODO here:
                        # - Read Controller temperature (self._kelly_motor_temp)
                        # - Read Motor temperature (self._kelly_controller_temp)
                        # - Read forward switch & backward switch (msg[5])
                        # - Verify forward and backward with status of command (msg[4])

                    elif (msg.arbitration_id == self._BATT_DATA_ID1):
                        packets_found += 1
                        self._batt_amps = msg.data[1]
                        self._batt_volts = msg.data[3]
                        self._batt_charge = msg.data[5]

                    elif (msg.arbitration_id == self._BATT_DATA_ID2):
                        packets_found += 1
                        self._batt_amps = msg.data[0]
                        self._batt_volts = msg.data[1]
                        self._batt_charge = msg.data[2]
                        self._batt_charge = msg.data[3]
                        self._batt_charge = msg.data[4]

                    elif (msg.arbitration_id == self._SOLAR_DATA_ID1):
                        packets_found += 1
                        # This packet gives _solar_amps_in and _solar_volts_in
                        # TODO: IMPLEMENTATION

                    elif (msg.arbitration_id == self._SOLAR_DATA_ID2):
                        packets_found += 1
                        # This packet gives _solar_volts_out
                        # TODO: IMPLEMENTATION NEEDED

                    elif (msg.arbitration_id == self._SOLAR_DATA_ID3):
                        packets_found += 1
                        # TODO: This packet gives _solar_pcb_temp and _solar_mosfet_temp
                        # IMPLEMENTATION NEEDED
                        
            GPIO.output(GPIOPin.CANBUS_IS_RUNNING, GPIO.LOW)
        except Exception:
            event_handler.bind(Event_.CANBUS_INTR)

    @property
    def data(self):
        return {
            'Gear' : self.gear,
            'MPH' : self.mph,
            'Kelly Motor Temp' : self.kelly_motor_temp,
            'Kelly Controller Temp' : self.kelly_controller_temp,
            'Errors' : self.error_code_readout,
            'Batt Temp Avg' : self.batt_temp_avg,
            'Batt Temp High' : self.batt_temp_high,
            'Batt Temp Low' : self.batt_temp_low,
            'Batt Temp High ID' : self.batt_temp_high_id,
            'Batt Temp Low ID' : self.batt_temp_low_id,
            'Batt Charge %' : self.batt_charge_perc,
            'Batt Volts' : self.batt_volts,
            'Batt Amps' : self.batt_amps,
            'Aux Volts' : self.aux_volts,
            'BPS Fault' : self.bpsfault,
            'Solar PCB Temp' : self.solar_pcb_temp,
            'Solar MOSFET Temp' : self.solar_mosfet_temp,
            'Solar Amps In' : self.solar_amps_in,
            'Solar Volts In' : self.solar_volts_in,
            'Solar Volts Out' : self.solar_volts_out,
        }

    @property
    def gear(self):
        return self._gear

    @property
    def mph(self):
        return self._mph

    @property
    def kelly_motor_temp(self):
        return self._kelly_motor_temp

    @property
    def kelly_controller_temp(self):
        return self._kelly_controller_temp

    @property
    def error_code_readout(self):
        return self._error_code_readout 

    @property
    def batt_temp_avg(self):
        return self._batt_temp_avg

    @property
    def batt_temp_high(self):
        return self._batt_temp_high

    @property
    def batt_temp_low(self):
        return self._batt_temp_low

    @property
    def batt_temp_high_id(self):
        return self._batt_temp_high_id

    @property
    def batt_temp_low_id(self):
        return self._batt_temp_low_id

    @property
    def batt_charge_perc(self):
        return self._batt_charge_perc

    @property
    def batt_volts(self):
        return self._batt_volts

    @property
    def batt_amps(self):
        return self._batt_amps

    @property
    def aux_volts(self):
        return self._aux_volts

    @property
    def bpsfault(self):
        return self._bpsfault

    @property
    def solar_pcb_temp(self):
        return self._solar_pcb_temp

    @property
    def solar_mosfet_temp(self):
        return self._solar_mosfet_temp

    @property
    def solar_amps_in(self):
        return self._solar_amps_in

    @property
    def solar_volts_in(self):
        return self._solar_volts_in

    @property
    def solar_volts_out(self):
        return self._solar_volts_out