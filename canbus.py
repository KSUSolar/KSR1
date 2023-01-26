#!/usr/bin/env python3

"""canbus.py: Retrieves hardware data from the 'can0' network interface."""

__author__      = "Aaron Harbin, Daniel Tebor"
__copyright__   = ""
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.3"
__maintainer__  = ""
__email__       = ""
__status__      = "Development"

import can
import os

from gpiozero import CPUTemperature
from threading import Thread


class CanBus(Thread):
    DEF_GEAR = 1

    DEF_BATT_CHARGE_PERC = 0
    DEF_BATT_VOLTS = 0
    DEF_BATT_AMPS = 0
    DEF_AUX_VOLTS = 0

    DEF_MPH = 0
    DEF_KELLY_MOTOR_TEMP = 0
    DEF_KELLY_CONTROLLER_TEMP = 0
    DEF_ERROR_CODE_READOUT = ""
    DEF_ERROR_CODES = [
        "0:Identification, ",
        "1:Over Volt, ",
        "2:Low Volt, ",
        "3:Reserved, ",
        "4:Stall, ",
        "5:InteralVolt, ",
        "6:Contr.OVERTEMP, ",
        "7:THR_ON_PWR, ",
        "8:Reserved2, ",
        "9:InternalReset,",
        "10:Hall-Open/Short, ",
        "11:AngleSensor, ",
        "12:Reserve3, ",
        "13:Reserve4, ",
        "14:MotorOVERTEMP, ",
        "15:Pi_Code_Error"
    ]

    DEF_BATT_TEMP_HIGH = 0
    DEF_BATT_TEMP_AVG = 0
    DEF_BATT_TEMP_LOW = 0
    DEF_BATT_HIGH_ID = 0 # This is the ID of the high temp thermistor
    DEF_BATT_LOW_ID = 0 # This is the ID of the low temp thermistor

    DEF_SOLAR_PCB_TEMP = 0
    DEF_SOLAR_MOSFET_TEMP = 0
    DEF_SOLAR_AMP_IN = 0
    DEF_SOLAR_VOLT_IN = 0
    DEF_SOLAR_VOLT_OUT = 0
    
    DEF_PI_TEMP = 0
    DEF_BPSFAULT = False

    def __init__(self):
        Thread.__init__(self)
        os.system('sudo ip link set can0 type can bitrate 500000') # Creates the canbus interface.
        os.system('sudo ifconfig can0 up') # Sarts the canbus interface.
        self._canbus = can.interface.Bus(interface = 'socketcan', channel = 'can0', baudrate = 500000)
        self._running = True

        self._gear = self.DEF_GEAR

        self._batt_charge_perc = self.DEF_BATT_CHARGE_PERC
        self._batt_volts = self.DEF_BATT_VOLTS
        self._batt_amps = self.DEF_BATT_AMPS
        self._aux_volts = self.DEF_AUX_VOLTS

        self._mph = self.DEF_MPH
        self._kelly_motor_temp = self.DEF_KELLY_MOTOR_TEMP
        self._kelly_controller_temp = self.DEF_KELLY_CONTROLLER_TEMP
        self._error_code_readout = self.DEF_ERROR_CODE_READOUT
        self._error_codes = self.DEF_ERROR_CODES

        self._batt_temp_high = self.DEF_BATT_TEMP_HIGH
        self._batt_temp_avg = self.DEF_BATT_TEMP_AVG
        self._batt_temp_low = self.DEF_BATT_TEMP_LOW
        self._batt_high_id = self.DEF_BATT_HIGH_ID
        self._batt_low_id = self.DEF_BATT_LOW_ID

        self._solar_pcb_temp = self.DEF_SOLAR_PCB_TEMP
        self._solar_mosfet_temp = self.DEF_SOLAR_MOSFET_TEMP
        self._solar_amp_in = self.DEF_SOLAR_AMP_IN
        self._solar_volt_in = self.DEF_SOLAR_VOLT_IN
        self._solar_volt_out = self.DEF_SOLAR_VOLT_OUT

        self._pi_temp = self.DEF_PI_TEMP
        self._bpsfault = self.DEF_BPSFAULT

    def run(self):
        ## These are BMS data packets about the battery ##
        BATT_DATA_ID1 = 1712
        BATT_DATA_ID2 = 1713

        ## These are motor controller packets about the motor and motor controller ##
        MOTOR_DATA_ID1 = 217128575
        MOTOR_DATA_ID2 = 404 # Don't know

        ## These are MPPT packets about the solar array ##
        """
            We don't know the packet IDs for the MPPTs yet because they're variable
            and we need to test it wired up with the full system.
        """
        SOLAR_DATA_ID1 = 404 # Don't know
        SOLAR_DATA_ID2 = 404 # Don't know
        SOLAR_DATA_ID3 = 404 # Don't know

        while self._running:
            data_found = False
        
            while not data_found and self._running:
                msg = self._canbus.recv()
                if (msg.arbitration_id == BATT_DATA_ID1):
                    data_found = True
                    self._batt_amps = msg.data[1]
                    self._batt_volts = msg.data[3]
                    self._batt_charge = msg.data[5]

            data_found = False

            while not data_found and self._running:
                print('ran')
                msg = self._canbus.recv()
                if (msg.arbitration_id == BATT_DATA_ID2):
                    data_found = True
                    self._batt_amps = msg.data[0]
                    self._batt_volts = msg.data[1]
                    self._batt_charge = msg.data[2]
                    self._batt_charge = msg.data[3]
                    self._batt_charge = msg.data[4]

            data_found = False

            while not data_found and self._running:
                msg = self._canbus.recv()
                if (msg.arbitration_id == MOTOR_DATA_ID1):
                    data_found = True
                    # This packets gives _mph and error codes
                    # I'm going to do my best to estimate the MPH but
                    # we're going to have to get more information from mechanical
                    # for this to be more exact
                    motor_rpm = ((msg[1] * 256) + msg.data[0]) / 10

                    # 14 teeth on the motor sprocket
                    # 47 teeth on the swing arm sprocket
                    # 0.3617 ratio
                    wheel_rpm = motor_rpm * 0.3617

                    # RPM to Linear Velocity formula
                    # v = r × RPM × 0.10472
                    self._mph = 0.3048 * wheel_rpm * 0.10472

                    # Reset Error Codes
                    self._error_code_readout = ""

                    # Error codes 1
                    error_code1 = bin(msg.data[6])[2:].zfill(8)
                    i = 7
                    while i >= 0:
                        if (error_code1[i] == "1"):
                            self._error_code_readout += self._error_codes[(i-7)*-1]
                        i -= 1
                    
                    # Error codes 2
                    i = 7
                    error_code2 = bin(msg.data[7])[2:].zfill(8)
                    while i >= 0:
                        if (error_code2[i] == "1"):
                            self._error_code_readout += self._error_codes[(i-15)*-1] 
                        i -= 1                           

            data_found = False

            while not data_found and self._running:
                print('ran')
                msg = self._canbus.recv()
                if (msg.arbitration_id == MOTOR_DATA_ID2):
                    data_found = True
                    # TODO here:
                    # - Read Controller temperature (self._kelly_motor_temp)
                    # - Read Motor temperature (self._kelly_controller_temp)
                    # - Read forward switch & backward switch (msg[5])
                    # - Verify forward and backward with status of command (msg[4])
            
            data_found = False

            while not data_found and self._running:
                print('ran')
                msg = self._canbus.recv()
                if (msg.arbitration_id == SOLAR_DATA_ID1):
                    data_found = True
                    # This packet gives _solar_amp_in and _solar_volt_in
                    # IMPLEMENTATION NEEDED

            data_found = False

            while not data_found and self._running:
                msg = self._canbus.recv()
                if (msg.arbitration_id == SOLAR_DATA_ID2):
                    data_found = True
                    # This packet gives _solar_volt_out
                    # IMPLEMENTATION NEEDED

            data_found = False

            while not data_found and self._running:
                msg = self._canbus.recv()
                if (msg.arbitration_id == SOLAR_DATA_ID3):
                    data_found = True
                    # This packet gives _solar_pcb_temp and _solar_mosfet_temp
                    # IMPLEMENTATION NEEDED
            
            self._pi_temp = CPUTemperature.temperature()

    def stop(self):
        self._running = False

    @property
    def gear(self):
        return self._gear

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

    # We don't need to return the "self._error_codes" list

    @property
    def batt_temp_high(self):
        return self._batt_temp_high

    @property
    def batt_temp_avg(self):
        return self._batt_temp_avg

    @property
    def batt_temp_low(self):
        return self._batt_temp_low

    @property
    def batt_high_id(self):
        return self._batt_high_id

    @property
    def batt_low_id(self):
        return self._batt_low_id

    @property
    def solar_pcb_temp(self):
        return self._solar_pcb_temp

    @property
    def solar_mosfet_temp(self):
        return self._solar_mosfet_temp

    @property
    def solar_amp_in(self):
        return self._solar_amp_in

    @property
    def solar_volt_in(self):
        return self._solar_volt_in

    @property
    def solar_volt_out(self):
        return self._solar_volt_out

    @property
    def pi_temp(self):
        return self._pi_temp

    @property
    def bpsfault(self):
        return self._bpsfault