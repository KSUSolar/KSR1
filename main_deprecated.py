import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import RPi.GPIO as GPIO
import threading
import time
import os
from gpiozero import CPUTemperature


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global mph_num
        global leftLight
        global rightLight
        global data_file

        super().__init__()
        self.beans = [0, 1, 2, 3, 4, 5, 6, 0]
        self.state_of_charge = self.beans[2]
        self.temperature = self.beans[5]
        self.amps = self.beans[3]
        self.volts = self.beans[1]
        self.auxV = self.beans[4]
        self.arTemp = self.beans[6]
        self.pTemp = CPUTemperature().temperature

        # setting grid layout which separates widget by row and column
        # QGrid is the layout for the application window
        self.centralGrid = QGridLayout()
        self.setLayout(self.centralGrid)

        self.SOC = QLabel('SOC: ' + str(self.state_of_charge))
        self.SOC.setStyleSheet('background-color: transparent;'
                         'color: white;'
                         'font-size: 30px;'
                         'font-style: bold;'
                         'text-align: left;'
                         'font-family:tahoma,geneva,sans-serif;')

        # Set left blinker icon
        self.Lblinkers = QLabel(self)
        self.Lblinkers.setText('⬅') # ◄ or ← or ⬅ # Boy do I love ASCII
        self.Lblinkers.setStyleSheet('color: green; font-size: 90px')
        self.Lblinkers.setAlignment(Qt.AlignCenter)

        # Set right blinker icon
        self.Rblinkers = QLabel(self)
        self.Rblinkers.setText('➡')
        self.Rblinkers.setStyleSheet('color: green; font-size: 90px')
        self.Rblinkers.setAlignment(Qt.AlignCenter)

        # Create the warning labels box
        self.warnings = QLabel('BPS Fault')
        self.warnings.setStyleSheet('background-color: transparent;' 'font-size: 25px;')
        self.warnings.setAlignment(Qt.AlignCenter)

        # Create the MPH box and both of its labels
        self.mph = QGroupBox()
        
        mphLabel = QLabel('MPH')
        mphLabel.setStyleSheet('font-family: verdana,geneva,sans-serif;' 'font-size: 40px;' 'color: #808080;')
        mphLabel.setAlignment(Qt.AlignHCenter)
        
        self.mphDisp = QLabel(str(mph_num))
        self.mphDisp.setStyleSheet('color:#FFFFFF;' 'font-family:tahoma,geneva,sans-serif;' 'font-size:40px;' 'font-weight: bold;')
        self.mphDisp.setAlignment(Qt.AlignHCenter)
        
        mphBox = QVBoxLayout()
        mphBox.addWidget(mphLabel)
        mphBox.addWidget(self.mphDisp)
        self.mph.setLayout(mphBox)

        # Create the box for temps
        self.tempSection = QGroupBox()

        self.battTemp = QLabel('Batt: ' +str(self.temperature) + ' °C')
        self.battTemp.setStyleSheet('color: white; font-size:20px; font-family:tahoma,geneva,sans-serif;')
        
        self.arrayTemp = QLabel('Array: ' + str(self.arTemp) + ' °C')
        self.arrayTemp.setStyleSheet('color: white; font-size:20px; font-family:tahoma,geneva,sans-serif;')

        self.piTemp = QLabel('Pi: ' + str(self.pTemp) + ' °C')
        self.piTemp.setStyleSheet('color: white; font-size:20px; font-family:tahoma,geneva,sans-serif;')

        tempBox = QGridLayout()
        tempBox.addWidget(self.battTemp, 0, 0)
        tempBox.addWidget(self.arrayTemp, 1, 0)
        tempBox.addWidget(self.piTemp, 2, 0)
        self.tempSection.setLayout(tempBox)

        # Create the box for  carStats and its labels & images
        self.carStats = QGroupBox()
        
        sinI = QLabel(self) ### Remove before flight ###
        pixmap2 = QPixmap('GUI_Images/icons8-sine-50.png')
        sinI.setPixmap(pixmap2)

        self.sinLabel = QLabel('Main: ' + str(self.amps) + ' A')
        self.sinLabel.setStyleSheet('color: white; font-size:20px; font-family:tahoma,geneva,sans-serif;')

        eleI = QLabel(self) ### Remove before flight ###
        pixmap3 = QPixmap('GUI_Images/icons8-main-electricity-52.png')
        eleI.setPixmap(pixmap3)

        self.eleLabel = QLabel('Main: ' + str(self.volts) + ' V')
        self.eleLabel.setStyleSheet('color: white; font-size:20px; font-family:tahoma,geneva,sans-serif;')

        auxI = QLabel(self) ### Remove before flight ###
        pixmap4 = QPixmap('GUI_Images/icons8-electricity-52.png')
        auxI.setPixmap(pixmap4)
        
        self.auxLabel = QLabel('Aux: ' + str(self.auxV) + ' V')
        self.auxLabel.setStyleSheet('color: white; font-size:20px; font-family:tahoma,geneva,sans-serif;')
        
        statBox = QGridLayout()
        #statBox.addWidget(sinI, 1, 0)
        statBox.addWidget(self.sinLabel, 1, 0)
        #statBox.addWidget(eleI, 0, 0)
        statBox.addWidget(self.eleLabel, 0, 0)
        #statBox.addWidget(auxI, 2, 0)
        statBox.addWidget(self.auxLabel, 2, 0)
        self.carStats.setLayout(statBox)

        # F N R
        self.FNR = QGroupBox()
        
        self.FLabel = QLabel('F')
        self.FLabel.setStyleSheet('color: white; font-size:80px; font-family:tahoma;')
        self.FLabel.setAlignment(Qt.AlignCenter)
        
        self.NLabel = QLabel('N')
        self.NLabel.setStyleSheet('color: white; font-size:80px; font-family:tahoma,geneva,sans-serif;')
        self.NLabel.setAlignment(Qt.AlignCenter)

        self.RLabel = QLabel('R')
        self.RLabel.setStyleSheet('color: white; font-size:80px; font-family:tahoma,geneva,sans-serif;')
        self.RLabel.setAlignment(Qt.AlignCenter)
        
        driveBox = QGridLayout()
        driveBox.addWidget(self.FLabel, 0, 0)
        driveBox.addWidget(self.NLabel, 0, 1)
        driveBox.addWidget(self.RLabel, 0, 2)
        self.FNR.setLayout(driveBox)
        
        # Placing all the widgets onto the main grid to display
        # column, row, rowspan,columnspan
        self.centralGrid.addWidget(self.SOC, 1, 0)
        self.centralGrid.addWidget(self.Lblinkers, 0, 0)
        self.centralGrid.addWidget(self.Rblinkers, 0, 2)
        self.centralGrid.addWidget(self.warnings, 2, 1)
        self.centralGrid.addWidget(self.mph, 1, 1)
        self.centralGrid.addWidget(self.carStats, 1, 0)
        self.centralGrid.addWidget(self.tempSection, 1, 2)
        self.centralGrid.addWidget(self.FNR, 0, 1)
                
        # make QTimer for everything else
        self.qTimer = QTimer(self)
        # set interval to 1 s
        self.qTimer.setInterval(1000) # 1000 ms = 1 s
        # connect timeout signal to signal handler
        self.qTimer.timeout.connect(self.getSensorValue)
        # start timer
        self.qTimer.start()
        
        # make QTimer for MPH
        self.qTimer2 = QTimer(self)
        # set interval to 1 s
        self.qTimer2.setInterval(250) # 1000 ms = 1 s
        # connect timeout signal to signal handler
        self.qTimer2.timeout.connect(self.getMPH)
        # start timer
        self.qTimer2.start()
        
        self.mainWidget = QGroupBox()
        self.mainWidget.setLayout(self.centralGrid)
        self.mainWidget.setStyleSheet("background-color: black;")
        self.mainWidget.setCursor(QCursor(Qt.CrossCursor))
        self.setCentralWidget(self.mainWidget) ###################################
        
        # MyMainWindow attributes
        self.setWindowTitle("SVT KSR1")
        self.showFullScreen()
        self.show()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.isFullScreen():
            self.showNormal()
            event.accept()
        elif event.key() == Qt.Key_Escape and (not self.isFullScreen()):
            self.showFullScreen()
            event.accept()
        elif (event.key() == Qt.Key_Q): # This is supposed to be able to kill the canBus & blinker threads but it just freezes the program.  I'm confused.
            self.close()
            
    def getSensorValue(self):
        # beans = recieve_message()
        # beans = [0, 1, 2, 3, 4, 5, 6]
        
        if (True):
            self.warnings.setStyleSheet('background-color: red; font-size: 25px;')
        
        self.state_of_charge += 1 # = beans[2]
        self.temperature += 1 # = beans[5]
        self.amps += 2 # = beans[3]
        self.volts += 3 # = beans[1]
        #mph_num += 1 # = beans[0]
        self.auxV += 1 # = beans[4]
        self.CPUTemp = str(CPUTemperature().temperature)

        self.SOC.setText('SOC: %d' %self.state_of_charge)
        #self.mphDisp.setText(str(mph_num))
        self.battTemp.setText('Batt: ' + str(self.temperature) + '°C')
        self.sinLabel.setText('Main: ' + str(self.amps) + ' A')
        self.eleLabel.setText('Main: ' + str(self.volts) + ' V')
        self.auxLabel.setText('Aux: ' + str(self.auxV) + ' V')
        self.piTemp.setText('Pi: ' + self.CPUTemp + ' °C')
        self.arrayTemp.setText('Array: ' + str(self.arTemp) + ' °C')
        
        # Log data to timestamped .csv
        data_file.write(f'{self.state_of_charge}, {self.amps}, {self.volts}, {self.auxV}, {self.CPUTemp}, {self.arTemp}\n')
        
        if (self.beans[7] == 0):
            self.FLabel.setStyleSheet('color: red; font-size:80px; font-family:tahoma;')
            self.RLabel.setStyleSheet('color: white; font-size:80px; font-family:tahoma;')
        elif (self.beans[7] == 1):
            self.NLabel.setStyleSheet('color: red; font-size:80px; font-family:tahoma;')
            self.FLabel.setStyleSheet('color: white; font-size:80px; font-family:tahoma;')
        elif (self.beans[7] == 2):
            self.RLabel.setStyleSheet('color: red; font-size:80px; font-family:tahoma;')
            self.NLabel.setStyleSheet('color: white; font-size:80px; font-family:tahoma;')
        
        if (self.beans[7] == 2):
            self.beans[7] = 0
        else:
            self.beans[7] += 1
    
    def getMPH(self):
        self.mphDisp.setText(str(mph_num))
        if (leftLight & rightLight):
            self.Lblinkers.show()
            self.Rblinkers.show()
        elif (leftLight):
            self.Lblinkers.show()
            self.Rblinkers.hide()
        elif (rightLight):
            self.Rblinkers.show()
            self.Lblinkers.hide()
        else:
            self.Rblinkers.hide()
            self.Lblinkers.hide()

class canBusThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global mph_num
        global alive

        while (alive):
            mph_num += 1
            time.sleep(0.4)
        print("canBus: Shutting Down")

class lightThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        global leftLight
        global rightLight
        global alive
        
        rightPin = 5
        leftPin = 6

        rightIn = 17
        leftIn = 27
        hazardIn = 22
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(5, GPIO.OUT)
        GPIO.setup(6, GPIO.OUT)
        GPIO.output(5, 0)
        GPIO.output(6, 0)
        print("GPIO output setup")

        GPIO.setup(rightIn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(leftIn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(hazardIn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        print("GPIO input setup")

        while (alive):
            if (GPIO.input(hazardIn) == 1):
                GPIO.output(rightPin, GPIO.HIGH)
                GPIO.output(leftPin, GPIO.HIGH)
                rightLight = True
                leftLight = True
                time.sleep(0.5)
                GPIO.output(rightPin, GPIO.LOW)
                GPIO.output(leftPin, GPIO.LOW)
                rightLight = False
                leftLight = False
                time.sleep(0.5)
            else:
                if (GPIO.input(rightIn) == 1):
                    GPIO.output(rightPin, GPIO.HIGH)
                    rightLight = True
                    time.sleep(0.5)
                    GPIO.output(rightPin, GPIO.LOW)
                    rightLight = False
                    time.sleep(0.5)
                else:
                    if (GPIO.input(leftIn) == 1):
                        GPIO.output(leftPin, GPIO.HIGH)
                        leftLight = True
                        time.sleep(0.5)
                        GPIO.output(leftPin, GPIO.LOW)
                        leftLight = False
                        time.sleep(0.5)
        print("Lights: Shutting Down")

if __name__ == '__main__':
    mph_num = 1
    leftLight = False
    rightLight = False
    alive = True
    
    os.system('sudo ip link set can0 type can bitrate 250000') # This sets up the canBus interface
    os.system('sudo ifconfig can0 up') # This starts said canBus interface
    
    canThread = canBusThread()
    canThread.start()
    
    lightT = lightThread()
    lightT.start()
    
    data_file = open (os.path.join(os.path.expanduser('~'), 'Desktop', "proofOfConcept", "Logged_Data", (time.strftime("%Y_%m_%d-%H_%m_%S") + ".csv")), "a")
    data_file.write(f'SOC, Main Amps, Main Volts, Aux Volts, Pi Temp, Array Temp\n')

    app = QApplication(sys.argv)
    ex = MyMainWindow()
    app.exec_()
    
    # This is as global variable that kills the canThread & lightThread
    alive = False
    canThread.join()
    lightT.join()
    print("Closed the threads")
    
    # Closing the file so all the data is written.
    data_file.close()