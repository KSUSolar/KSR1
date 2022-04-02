import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from gui_variables import *
from parsed_can_message import *
from data_parser import *
from log_data import *
import time
from datetime import datetime
import os

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.time = QTime.currentTime()
        self.setStyleSheet("background-color: black;")
        self.setCursor(QCursor(Qt.CrossCursor))
        
        
        self.initUI()

    def initUI(self):
        # set central widget
        self.centralGrid = MainGrid()
        self.setCentralWidget(self.centralGrid)

        # time is shown in status bar
        self.statusbar = self.statusBar()
        self.statusbar.showMessage(self.time.toString(Qt.DefaultLocaleLongDate))
        self.statusbar.setStyleSheet('background-color: pink')
        
        # MyMainWindow attributes
        self.setWindowTitle("KSU SVT")
        MyMainWindow.resize(self, 480, 272)
        self.setFixedSize(480, 272)
        self.showFullScreen()
        self.show()
        
        # log data
        logData()
        
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.isFullScreen():
            self.showNormal()
            event.accept()
        elif event.key() == Qt.Key_Escape and (not self.isFullScreen()):
            self.showFullScreen()
            event.accept()

    # centers the widget in the screen
    def center(self):
        # frameGeometry gets the location and size of the window
        qr = self.frameGeometry()
        # finds out the center location for the monitor you are using
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class MainGrid(QWidget):
    def __init__(self):
        super().__init__()
        self.battery_percentage = battery_percentage
        self.KW_usage = KW_usage
        self.mph = mph
        self.temperature = temperature
        self.amps = amps
        self.volts = volts
        self.mph_num = mph_num
        self.initGrid()

    def initGrid(self):
        # setting grid layout which seperates widget by row and column
        # QGrid is the layout for the application window
        grid = QGridLayout()
        self.setLayout(grid)
        # attributes for widgets
        self.batteryPercentage = QLabel(
            "<html><head/><body><p><span style=' font-size:40px; color:#ffffff;'>     {battery_percentage} % </span></p></body></html>".format(
                battery_percentage=battery_percentage))
        
        
        self.batteryPercentage = QLabel("""
        <html>
        <head>
            <title></title>
        </head>
        <body data-gr-ext-installed="" data-new-gr-c-s-check-loaded="14.1000.0" data-new-gr-c-s-loaded="14.1000.0">
        <p style="text-align: left;"><span style="color:#FFFFFF;"><span style="font-size:30px;"><span style="font-family:tahoma,geneva,sans-serif;">    {KW_usage} KW</span></span></p>
        </body>
        </html>

        """)   
           
           
           
                
        self.batteryPercentage.setStyleSheet('background-color: transparent;'
                         'color: white;'
                         'font-size: 35px;'
                         'font-style: bold;')

        tempIcon = QLabel("""
        <html>
        <head>
            <title></title>
        </head>
        <body data-gr-ext-installed="" data-new-gr-c-s-check-loaded="14.1000.0" data-new-gr-c-s-loaded="14.1000.0">
        <p style="text-align: right;"><img src="GUI_Images/icons8-thermometer-40.png"/></p>
        </body>
        </html>

        """)
        tempIcon.setStyleSheet('background-color: transparent;'
                               'font-size: 25px;')

        headLightIcon = QLabel("""
        <html>
        <head>
            <title></title>
        </head>
        <body data-gr-ext-installed="" data-new-gr-c-s-check-loaded="14.1000.0" data-new-gr-c-s-loaded="14.1000.0">
        <p style="text-align: right;"><img src="GUI_Images/icons8-headlight-50.png"/></p>
        </body>
        </html>

        """)
        headLightIcon.setStyleSheet('background-color: transparent;'
                                    'font-size: 25px;')

        chargeIcon = QLabel("""
        <html>
        <head>
            <title></title>
        </head>
        <body data-gr-ext-installed="" data-new-gr-c-s-check-loaded="14.1000.0" data-new-gr-c-s-loaded="14.1000.0">
        <p style="text-align: center;"><img src="GUI_Images/icons8-charging-station-50.png"/></p>
        </body>
        </html>

        """)
        chargeIcon.setStyleSheet('background-color: transparent;'
                                 'font-size: 25px;')

        KWProgBar = QLabel('KW Progress Bar ')
        KWProgBar.setStyleSheet('background-color: transparent')
        progBar = QProgressBar()
        progBar.setMaximum(1000)
        progBar.setValue(300)
        progBar.setAlignment(Qt.AlignCenter)
        progBar.setStyleSheet('QProgressBar::chunk.setStyleSheet'
                            '{'
                            'background-color: white;'
                            '}')
        progBar.setStyleSheet('background-color: transparent;'
                            'max-height: 25px;'
                            'min-height: 25px;'
                            'border: 2px solid white;'
                            'border-radius: 6px;'
                            )

        self.KW = QLabel("""
        <html>
        <head>
            <title></title>
        </head>
        <body data-gr-ext-installed="" data-new-gr-c-s-check-loaded="14.1000.0" data-new-gr-c-s-loaded="14.1000.0">
        <p style="text-align: left;"><span style="color:#FFFFFF;"><span style="font-size:30px;"><span style="font-family:tahoma,geneva,sans-serif;">    {KW_usage} KW</span></span></p>
        </body>
        </html>

        """.format(KW_usage=KW_usage))
        self.KW.setStyleSheet('background-color: transparent;'
                         'color: white;'
                         'font-size: 35px;'
                         'font-style: bold;')

        Lblinkers = QLabel("""
        <html>
        <head>
            <title></title>
        </head>
        <body data-gr-ext-installed="" data-new-gr-c-s-check-loaded="14.1000.0" data-new-gr-c-s-loaded="14.1000.0">
        <p style="text-align: center;"><img src="GUI_Images/icons8-arrow-pointing-left-48.png"/></p>
        </body>
        </html>

        """)
        Lblinkers.setStyleSheet('background-color: transparent;'
                                'font-size: 25px;')

        Rblinkers = QLabel("""
        <html>
        <head>
            <title></title>
        </head>
        <body data-gr-ext-installed="" data-new-gr-c-s-check-loaded="14.1000.0" data-new-gr-c-s-loaded="14.1000.0">
        <p style="text-align: center;"><img src="GUI_Images/icons8-arrow-pointing-right-48.png"/></p>
        </body>
        </html>

        """)
        Rblinkers.setStyleSheet('background-color: transparent;'
                                'font-size: 25px;')

        warnings = QLabel('Warnings')
        warnings.setStyleSheet('background-color: red;'
                               'font-size: 25px;')

        self.mph = QLabel("""
        <html>
        <head>
            <title></title>
        </head>
        <body data-gr-ext-installed="" data-new-gr-c-s-check-loaded="14.1000.0" data-new-gr-c-s-loaded="14.1000.0">
        <p style="text-align: center;"><span style="font-family:verdana,geneva,sans-serif;"><span style="font-size:40px;"><span style="color:#808080;">MPH</span></span></span></p>

        <p style="text-align: center;"><span style="color:#FFFFFF;"><span style="font-family:tahoma,geneva,sans-serif;"><strong><span style="font-size:40px;">{mph_num}</span></strong></span></span></p>
        </body>
        </html>

        """.format(mph_num=mph_num))
        self.mph.setStyleSheet('background-color: transparent')

        self.carStats = QLabel("""
        <html>
        <head>
            <title></title>
        </head>
        <body data-gr-ext-installed="" data-new-gr-c-s-check-loaded="14.1000.0" data-new-gr-c-s-loaded="14.1000.0">
        <p style="text-align: left;"><img src="GUI_Images/icons8-temperature-40.png"/><span style="color:#FFFFFF;"><span style="font-size:20px;"><span style="font-family:tahoma,geneva,sans-serif;">    {temperature} &deg;F</span></span></p>

        <p style="text-align: left;"><img src="GUI_Images/icons8-sine-40.png"/><span style="color:#FFFFFF;"><span style="font-size:20px;"><span style="font-family:tahoma,geneva,sans-serif;">   {amps} A</span></span></p>

        <p style="text-align: left;"><img src="GUI_Images/icons8-electricity-40.png"/><span style="color:#FFFFFF;"><span style="font-size:20px;"><span style="font-family:tahoma,geneva,sans-serif;">&nbsp;   {volts} V</span></span></p>
        </body>
        </html>

        """.format(temperature=temperature, amps=amps, volts=volts))
        self.carStats.setStyleSheet('background-color: transparent')
        # adding batteryPercentage as a widget
        # batteryPercentage will be added to MyMainApplication window
        # column, row, rowspan,columnspan
        grid.addWidget(self.batteryPercentage, 3, 0, 2, 0)
        grid.addWidget(tempIcon, 0, 2, 2, 1)
        grid.addWidget(headLightIcon, 0, 3, 2, 1)
        grid.addWidget(chargeIcon, 0, 4, 2, 1)
        
        
        grid.addWidget(self.KW, 4, 0, 2, 0)
        grid.addWidget(Lblinkers, 3, 1, 2, 1)
        grid.addWidget(Rblinkers, 3, 2, 2, 1)
        grid.addWidget(warnings, 6, 0, 2, 1)
        grid.addWidget(self.mph, 5, 1, 3, 2)
        grid.addWidget(self.carStats, 3, 3, 6, 2)
        
        # get current time and date
        starttime = time.time()
        now = datetime.now()
        
        # concatenate information for logData() to create new file
        save_path = '/Solar Racer/Logged_Data'
        file_name = now.strftime("%Y") + "-" + now.strftime("%m") + "-" + now.strftime("%d") + ".txt"
        completeFileName = os.path.join(save_path, file_name)
        
        # open / create new readable / writeable txt file (called name concatenated above)
        fh = open(completeFileName, 'w+')
        
        # make DataTimer
        self.dataTimer = QTimer(self)
        # set interval to 10 m
        self.dataTimer.setInterval(600000) # 1000 ms = 1 s
        # connect timeout signal to signal handler
        self.dataTimer.timeout.connect(self.logData(fh))
        # start data timer
        self.dataTimer.start()
        
        # make QTimer
        self.qTimer = QTimer(self)
        # set interval to 1 s
        self.qTimer.setInterval(1000) # 1000 ms = 1 s
        # connect timeout signal to signal handler
        self.qTimer.timeout.connect(self.getSensorValue)
        # start timer
        self.qTimer.start()

    def getSensorValue(self):
        #data = recieve_message()
        #self.temperature.setText('%d &deg F' % self.temperature)
        #self.batteryPercentage.setText('%d \N{DEGREE SIGN} C' % self.temperature)
        self.KW_usage += 1
        self.KW.setText('%d KW' %self.KW_usage)
        self.batteryPercentage.setText('%d' %self.KW_usage)
        
    def logData(self, file_handler):
        fh = file_handler
        # get current time and date
        starttime = time.time()
        now = datetime.now()
        # write data in txt file
        fh.write(now.strftime("%H:%M:%S") + " -- " ) # log remainder of data following h:m:s --  def log_data(self):
        

if __name__ == '__main__':
    import sys

    #MainGrid.initGrid.mph.hide()
    app = QApplication(sys.argv)
    ex = MyMainWindow()
    sys.exit(app.exec_())
