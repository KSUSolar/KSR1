#!/usr/bin/env python3

"""gui.py: Car dashboard. Displays telemetry."""

__author__      = "Daniel Tebor"
__copyright__   = "Copyright 2022 Solar Vehicle Team at KSU"
__credits__     = ["Aaron Harbin, Daniel Tebor"]

__license__     = "GPL"
__version__     = "1.0.7"
__maintainer__  = "Aaron Harbin, Daniel Tebor"
__email__       = "solarvehicleteam@kennesaw.edu"
__status__      = "Development"

from common import pi_tm as pi
from common.event import Event_
from core import event_handler
from core.light_controller import LightController
from daemons.canbus import CANBus
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class GUI(QMainWindow):
    
    def __init__(self, canbus: CANBus):
        super().__init__(parent = None)
        self._canbus = canbus

        # Create the box for the Gearbox: F N R.
        gearbox_box = QGroupBox()
        
        self._fgear_display = QLabel('F')
        self._fgear_display.setStyleSheet(
            'color: white;'
            'font-family: tahoma, geneva, sans-serif;'
            'font-size: 80px;'
            )
        self._fgear_display.setAlignment(Qt.AlignCenter)
        
        self._ngear_display = QLabel('N')
        self._ngear_display.setStyleSheet(
            'color: white;'
            'font-family: tahoma, geneva, sans-serif;'
            'font-size: 80px;')
        self._ngear_display.setAlignment(Qt.AlignCenter)

        self._rgear_display = QLabel('R')
        self._rgear_display.setStyleSheet(
            'color: white;'
            'font-family: tahoma, geneva, sans-serif;'
            'font-size: 80px;'
            )
        self._rgear_display.setAlignment(Qt.AlignCenter)
        
        gearbox_layout = QGridLayout()
        gearbox_layout.addWidget(self._fgear_display, 0, 0)
        gearbox_layout.addWidget(self._ngear_display, 0, 1)
        gearbox_layout.addWidget(self._rgear_display, 0, 2)
        gearbox_box.setLayout(gearbox_layout)


        # Sets left blinker icon.
        self._l_blinker = QLabel('⬅')  # ◄ or ← or ⬅ #.  Boy do I love ASCII.
        self._l_blinker.setStyleSheet('color: green; font-size: 90px')
        self._l_blinker.setAlignment(Qt.AlignCenter)


        # Sets right blinker icon.
        self._r_blinker = QLabel('➡')
        self._r_blinker.setStyleSheet('color: green; font-size: 90px')
        self._r_blinker.setAlignment(Qt.AlignCenter)


        # Creates the batt charge display.
        self._battcharge = QLabel(
            'SOC: ' + str(self._canbus.batt_charge_perc) + '%')
        self._battcharge.setStyleSheet(
            'background-color: transparent;'
            'color: white;'
            'font-family: tahoma, geneva,sans-serif;'
            'font-size: 30px;'
            'font-style: bold;'
            'text-align: left;'
            )


        # Creates the car stats display.
        battstats_box = QGroupBox()

        self._batt_volts_display = QLabel(
            'Batt Voltage: ' + str(self._canbus.batt_volts) + 'V')
        self._batt_volts_display.setStyleSheet(
            'color: white;'
            'font-family: tahoma, geneva, sans-serif;'
            'font-size: 20px;'
            )

        self._batt_amps_display = QLabel(
            'Batt Current: ' + str(self._canbus.batt_amps) + 'A')
        self._batt_amps_display.setStyleSheet(
            'color: white;'
            ' font-family: tahoma, geneva, sans-serif;'
            'font-size: 20px;'
            )

        self._aux_volts_display = QLabel(
            'Aux Voltage: ' + str(self._canbus.aux_volts) + 'V')
        self._aux_volts_display .setStyleSheet(
            'color: white;'
            'font-family: tahoma, geneva, sans-serif;'
            'font-size: 20px;'
            )
        
        battstats_layout = QGridLayout()
        battstats_layout.addWidget(self._batt_volts_display , 0, 0)
        battstats_layout.addWidget(self._batt_amps_display, 1, 0)
        battstats_layout.addWidget(self._aux_volts_display, 2, 0)
        battstats_box.setLayout(battstats_layout)


        # Creates the MPH display.
        mph_box = QGroupBox()
        
        mph_label = QLabel('MPH')
        mph_label.setStyleSheet(
            'color: #808080;'
            'font-family: verdana, geneva, sans-serif;'
            'font-size: 40px;'
            )
        mph_label.setAlignment(Qt.AlignHCenter)
        
        self._mph_display = QLabel(str(self._canbus.mph))
        self._mph_display.setStyleSheet(
            'color: #FFFFFF;'
            'font-family: tahoma, geneva, sans-serif;'
            'font-size: 40px;'
            'font-weight: bold;'
            )
        self._mph_display.setAlignment(Qt.AlignHCenter)
        
        mph_layout = QVBoxLayout()
        mph_layout.addWidget(mph_label)
        mph_layout.addWidget(self._mph_display)
        mph_box.setLayout(mph_layout)


        # Creates the hardware temps display.
        temps_box = QGroupBox()

        self._batt_temp_display = QLabel(
            'batt: ' + str(self._canbus.batt_temp_avg) + '°C')
        self._batt_temp_display.setStyleSheet(
            'color: white;'
            'font-family: tahoma, geneva, sans-serif;'
            'font-size: 20px;'
            )
        
        self._solar_temp_display = QLabel(
            'Solar Array: ' + str(self._canbus.solar_pcb_temp) + '°C')
        self._solar_temp_display.setStyleSheet(
            'color: white;'
            'font-family: tahoma, geneva, sans-serif;'
            'font-size: 20px;'
            )

        self._pi_temp_display = QLabel(
            'Pi: ' + str(pi.temp()) + '°C')
        self._pi_temp_display.setStyleSheet(
            'color: white;'
            'font-family: tahoma, geneva, sans-serif;'
            'font-size: 20px;'
            )

        temps_layout = QGridLayout()
        temps_layout.addWidget(self._batt_temp_display, 0, 0)
        temps_layout.addWidget(self._solar_temp_display, 1, 0)
        temps_layout.addWidget(self._pi_temp_display, 2, 0)
        temps_box.setLayout(temps_layout)


        # Creates the BPS Fault warning display.
        self._bpsfault_warning = QLabel('BPS Fault')
        self._bpsfault_warning.setStyleSheet(
            'background-color: transparent;'
            'font-size: 25px;'
            )
        self._bpsfault_warning.setAlignment(Qt.AlignCenter)


        # Creates the main GUI layout.
        gui_layout = QGridLayout()

        # Places all the widgets onto the gui layout.
        # column, row, rowspan,columnspan.
        gui_layout.addWidget(self._l_blinker, 0, 0)
        gui_layout.addWidget(gearbox_box, 0, 1)
        gui_layout.addWidget(self._r_blinker, 0, 2)
        gui_layout.addWidget(self._battcharge, 1, 0)
        gui_layout.addWidget(battstats_box, 1, 0)
        gui_layout.addWidget(mph_box, 1, 1)
        gui_layout.addWidget(temps_box, 1, 2)
        gui_layout.addWidget(self._bpsfault_warning, 2, 1)
        
        # Makes main gui box.
        gui_box = QGroupBox()
        gui_box.setStyleSheet("background-color: black;")
        gui_box.setLayout(gui_layout)
        #gui_box.setCursor(QCursor(Qt.CrossCursor))
        self.setCentralWidget(gui_box)

        # Sets GUI attributes.
        self.setWindowTitle("SVT KSR1")
        self.setStyleSheet("background-color: black;")
        #self.setCursor(QCursor(Qt.CrossCursor))

    def show_(self):
        #self.showFullScreen()
        self.show()

    def close_(self):
        self.close()
        event_handler.bind(Event_.GUI_CLOSE)

    def _update(self):
        self._update_gearbox(self._canbus.gear)
        self._update_blinkers(
            LightController.l_blinker_light_on, 
            LightController.r_blinker_light_on
            )
        self._update_battcharge(self._canbus.batt_charge_perc)
        self._update_battstats(
            self._canbus.batt_volts,
            self._canbus.batt_amps,
            self._canbus.aux_volts
            )
        self._update_mph(self._canbus.mph)
        self._update_temps(self._canbus.batt_temp_avg,
            self._canbus.solar_pcb_temp,
            pi.CPUTemperature
            )
        self._update_bpsfault_warning(self._canbus.bpsfault)
        
        self.update()

    def _update_gearbox(self, gear):
        """Updates the gearbox GUI elements
        Keyword arguements:
        gear -- the selected gear; ranges 0 - 2
        """
        if (gear == 0):
            self._fgear_display.setStyleSheet(
                'color: red;'
                'font-family: tahoma, geneva, sans-serif;'
                'font-size: 80px;'
                )
            self._ngear_display.setStyleSheet(
                'color: white;'
                'font-family: tahoma, geneva, sans-serif;'
                'font-size: 80px;'
                )
            self._rgear_display.setStyleSheet(
                'color: white;'
                'font-family: tahoma, geneva, sans-serif;'
                'font-size: 80px;'
                )
        elif (gear == 1):
            self._fgear_display.setStyleSheet(
                'color: white;'
                'font-family: tahoma, geneva, sans-serif;'
                'font-size: 80px;'
                )
            self._ngear_display.setStyleSheet(
                'color: red;'
                'font-family: tahoma, geneva, sans-serif;'
                'font-size: 80px;'
                )
            self._rgear_display.setStyleSheet(
                'color: white;'
                'font-family: tahoma, geneva, sans-serif;'
                'font-size: 80px;'
                )
        elif (gear == 2):
            self._fgear_display.setStyleSheet(
                'color: white;'
                'font-family: tahoma, geneva, sans-serif;'
                'font-size: 80px;'
                )
            self._ngear_display.setStyleSheet(
                'color: white;'
                'font-family: tahoma, geneva, sans-serif;'
                'font-size: 80px;'
                )
            self._rgear_display.setStyleSheet(
                'color: red;'
                'font-family: tahoma, geneva, sans-serif;'
                'font-size: 80px;'
                )

    def _update_blinkers(self, l_blinker_on, r_blinker_on):
        """Updates the left blinker and right blinker GUI elements.
        Keyword arguments:
        l_blinker_on -- True if blinker is on, False if blinker is off
        r_blinker_on -- True if blinker is on, False if blinker is off
        """
        if l_blinker_on and r_blinker_on:
            self._l_blinker.show()
            self._r_blinker.show()
        elif l_blinker_on:
            self._l_blinker.show()
            self._r_blinker.hide()
        elif r_blinker_on:
            self._l_blinker.hide()
            self._r_blinker.show()
        else:
            self._l_blinker.hide()
            self._r_blinker.hide()
    
    def _update_battcharge(self, charge_percent):
        """Updates the batt charge GUI element.
        Keyword arguments:
        batt_percent -- percent charge of the main batt; ranges 0 - 100
        """
        self._battcharge.setText('SOC: %d' %charge_percent)

    def _update_battstats(self, batt_volts, batt_amps, aux_volts):
        """Updates the car stats GUI element.
        Keyword arguments:
        batt_volts -- main batt voltage
        batt_amps -- main batt current
        aux_volts -- aux batt voltage
        """
        self._batt_volts_display.setText('Batt Voltage: ' + str(batt_volts) + 'V')
        self._batt_amps_display.setText("Batt Current" + str(batt_amps) + 'A')
        self._aux_volts_display.setText('Aux Voltage: ' + str(aux_volts) + 'V')

    def _update_mph(self, mph):
        """Updates the MPH GUI element.
        Keyword arguments:
        mph -- speed of the car in miles per hour
        """
        self._mph_display.setText(str(mph))

    def _update_temps(self, batt_temp, solar_temp, pi_temp):
        """Updates the temperatures GUI element.
        Keyword arguments:
        batt_temp -- temperature, in celcius, of the batt
        solar_temp -- temperature, in celcius, of the solar array
        pi_temp -- temperature, in celcius, of the raspberry pi cpu
        """
        self._batt_temp_display.setText('batt: ' + str(batt_temp) + '°C')
        self._solar_temp_display.setText('Solar Arr: ' + str(solar_temp) + '°C')
        self._pi_temp_display.setText('Pi: ' + str(pi_temp) + '°C')

    def _update_bpsfault_warning(self, bpsfault):
        """Updates the BPS Fault warning GUI element.
        Keyword elements:
        bpsfault -- True if there is a BPS Fault, False id there is not
        """
        if (bpsfault):
            self._bpsfault_warning.setStyleSheet('background-color: red;' 'font-size: 25px;')
        else:
            self._bpsfault_warning.setStyleSheet('background-color: transparent;' 'font-size: 25px;')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.isFullScreen():
            self.showNormal()
            event.accept()
        elif event.key() == Qt.Key_Escape and (not self.isFullScreen()):
            self.showFullScreen()
            event.accept()
        elif (event.key() == Qt.Key_Escape):
            # Shuts down Program
            print('ran')
            self.close_()