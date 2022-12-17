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
    DEF_BATT_TEMP_HIGH = 0
    DEF_BATT_TEMP_AVG = 0
    DEF_BATT_TEMP_LOW = 0
    DEF_BATT_HIGH_ID = 0 # This is the ID of the high temp thermistor
    DEF_BATT_LOW_ID = 0 # This is the ID of the low temp thermistor
    DEF_SOLAR_TEMP = 0
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
        self._batt_temp_high = self.DEF_BATT_TEMP_HIGH
        self._batt_temp_avg = self.DEF_BATT_TEMP_AVG
        self._batt_temp_low = self.DEF_BATT_TEMP_LOW
        self._solar_temp = self.DEF_SOLAR_TEMP
        self._pi_temp = self.DEF_PI_TEMP
        self._bpsfault = self.DEF_BPSFAULT

    def run(self):
        BATT_DATA_ID = 1712
        SOLAR_DATA_ID = 3008

        while self._running:
            ## These are BMS data packets about the battery ##
            BATT_DATA_ID1 = 1712
            BATT_DATA_ID2 = 1713

            ## These are motor controller packets about the motor and motor controller ##
            MOTOR_DATA_ID1 = 217128575
            MOTOR_DATA_ID2 = 404

            ## These are MPPT packets about the solar array ##
            """
                We don't know the packet IDs for the MPPTs yet because they're variable
                and we need to test it wired up with the full system.
            """
            SOLAR_DATA_ID1 = 404
            SOLAR_DATA_ID2 = 404
            SOLAR_DATA_ID3 = 404

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

            while not data_found:
                msg = self._canbus.recv()
                if (msg.arbitration_id == MOTOR_DATA_ID1):
                    data_found = True
                    # 14 teeth on the motor sprocket
                    # ?? teeth on the swing arm sprocket
                    # IMPLEMENTATION NEEDED

            data_found = False

            while not data_found and self._running:
                print('ran')
                msg = self._canbus.recv()
                if (msg.arbitration_id == MOTOR_DATA_ID2):
                    data_found = True
                    # 14 teeth on the motor sprocket
                    # ?? teeth on the swing arm sprocket
                    # IMPLEMENTATION NEEDED
            
            data_found = False

            while not data_found and self._running:
                print('ran')
                msg = self._canbus.recv()
                if (msg.arbitration_id == SOLAR_DATA_ID1):
                    data_found = True
                    # IMPLEMENTATION NEEDED

            data_found = False

            while not data_found:
                msg = self._canbus.recv()
                if (msg.arbitration_id == SOLAR_DATA_ID2):
                    data_found = True
                    # 14 teeth on the motor sprocket
                    # ?? teeth on the swing arm sprocket
                    # IMPLEMENTATION NEEDED

            data_found = False

            while not data_found:
                msg = self._canbus.recv()
                if (msg.arbitration_id == SOLAR_DATA_ID3):
                    data_found = True
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
    def batt_temp(self):
        return self._batt_temp

    @property
    def solar_temp(self):
        return self._solar_temp

    @property
    def pi_temp(self):
        return self._pi_temp

    @property
    def bpsfault(self):
        return self._bpsfault