import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from test import update

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.time = QTime.currentTime()
        self.setStyleSheet("background-color: black;")
        self.setCursor(QCursor(Qt.CrossCursor))
        self.initUI()

    def initUI(self):
        # set central widget
        centralGrid = MainGrid()
        self.setCentralWidget(centralGrid)

        # time is shown in status bar
        self.statusbar = self.statusBar()
        self.statusbar.showMessage(self.time.toString(Qt.DefaultLocaleLongDate))
        self.statusbar.setStyleSheet('background-color: pink')

        # MyMainWindow attributes
        self.setWindowTitle("KSU SVT")
        MyMainWindow.resize(self, 800, 500)
        #self.showFullScreen()
        self.show()

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
        self.initGrid()

    def initGrid(self):
        battery_percentage = 50
        KW_usage = 833
        mph = 80
        temperature = 90.8
        amps = 200.6
        volts = 50.1

        # setting grid layout which seperates widget by row and column
        # QGrid is the layout for the application window
        grid = QGridLayout()
        self.setLayout(grid)
        # attributes for widgets
        batteryPercentage = QLabel(
            "<html><head/><body><p><img src='/home/debian/Desktop/SVT GUI/icons8-lightning-bolt-52.png'/><span style=' font-size:65px; color:#ffffff;'>     {battery_percentage} % </span></p></body></html>".format(
                battery_percentage=battery_percentage))
        batteryPercentage.setStyleSheet('background-color: transparent;')

        tempIcon = QLabel("""
        <html>
        <head>
            <title></title>
        </head>
        <body data-gr-ext-installed="" data-new-gr-c-s-check-loaded="14.1000.0" data-new-gr-c-s-loaded="14.1000.0">
        <p style="text-align: right;"><img src="/home/debian/Desktop/SVT GUI/icons8-thermometer-50.png"/></p>
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
        <p style="text-align: right;"><img src="/home/debian/Desktop/SVT GUI/icons8-headlight-50.png"/></p>
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
        <p style="text-align: center;"><img src="/home/debian/Desktop/SVT GUI/icons8-charging-station-50.png"/></p>
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
                            'max-height: 50px;'
                            'min-height: 50px;'
                            'border: 2px solid white;'
                            'border-radius: 6px;'
                            )

        KW = QLabel("""
        <html>
        <head>
            <title></title>
        </head>
        <body data-gr-ext-installed="" data-new-gr-c-s-check-loaded="14.1000.0" data-new-gr-c-s-loaded="14.1000.0">
        <p style="text-align: left;"><span style="color:#FFFFFF;"><span style="font-size:40px;"><span style="font-family:tahoma,geneva,sans-serif;">    {KW_usage} KW</span></span></p>
        </body>
        </html>

        """.format(KW_usage=KW_usage))
        KW.setStyleSheet('background-color: transparent;'
                         'color: white;'
                         'font-size: 35px;'
                         'font-style: bold;')

        Lblinkers = QLabel("""
        <html>
        <head>
            <title></title>
        </head>
        <body data-gr-ext-installed="" data-new-gr-c-s-check-loaded="14.1000.0" data-new-gr-c-s-loaded="14.1000.0">
        <p style="text-align: center;"><img src="/home/debian/Desktop/SVT GUI/icons8-arrow-pointing-left-96"/></p>
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
        <p style="text-align: center;"><img src="/home/debian/Desktop/SVT GUI/icons8-arrow-pointing-right-96"/></p>
        </body>
        </html>

        """)
        Rblinkers.setStyleSheet('background-color: transparent;'
                                'font-size: 25px;')

        warnings = QLabel('Warnings')
        warnings.setStyleSheet('background-color: red;'
                               'font-size: 25px;')

        mph = QLabel("""
        <html>
        <head>
            <title></title>
        </head>
        <body data-gr-ext-installed="" data-new-gr-c-s-check-loaded="14.1000.0" data-new-gr-c-s-loaded="14.1000.0">
        <p style="text-align: center;"><span style="font-family:verdana,geneva,sans-serif;"><span style="font-size:50px;"><span style="color:#808080;">MPH</span></span></span></p>

        <p style="text-align: center;"><span style="color:#FFFFFF;"><span style="font-family:tahoma,geneva,sans-serif;"><strong><span style="font-size:172px;">{mph}</span></strong></span></span></p>
        </body>
        </html>

        """.format(mph=mph))
        mph.setStyleSheet('background-color: transparent')

        carStats = QLabel("""
        <html>
        <head>
            <title></title>
        </head>
        <body data-gr-ext-installed="" data-new-gr-c-s-check-loaded="14.1000.0" data-new-gr-c-s-loaded="14.1000.0">
        <p style="text-align: left;"><img src="/home/debian/Desktop/SVT GUI/icons8-temperature-100.png"/><span style="color:#FFFFFF;"><span style="font-size:60px;"><span style="font-family:tahoma,geneva,sans-serif;">    {temperature} &deg;F</span></span></p>

        <p style="text-align: left;"><img src="/home/debian/Desktop/SVT GUI/icons8-sine-96.png"/><span style="color:#FFFFFF;"><span style="font-size:60px;"><span style="font-family:tahoma,geneva,sans-serif;">   {amps} A</span></span></p>

        <p style="text-align: left;"><img src="/home/debian/Desktop/SVT GUI/icons8-electricity-96.png"/><span style="color:#FFFFFF;"><span style="font-size:60px;"><span style="font-family:tahoma,geneva,sans-serif;">&nbsp;   {volts} V</span></span></p>
        </body>
        </html>

        """.format(temperature=temperature, amps=amps, volts=volts))
        carStats.setStyleSheet('background-color: transparent')

        # adding batteryPercentage as a widget
        # batteryPercentage will be added to MyMainApplication window
        # column, row, rowspan,columnspan
        grid.addWidget(batteryPercentage, 0, 1, 1, 1)
        grid.addWidget(tempIcon, 0, 2, 1, 1)
        grid.addWidget(headLightIcon, 0, 3, 1, 1)
        grid.addWidget(chargeIcon, 0, 4, 1, 1)
        # grid.addWidget(KWProgBar, 3, 1, 1, 3)
        grid.addWidget(progBar, 3, 1, 1, 3)
        grid.addWidget(KW, 3, 4, 1, 1)
        grid.addWidget(Lblinkers, 4, 2, 1, 1)
        grid.addWidget(Rblinkers, 4, 3, 1, 1)
        grid.addWidget(warnings, 5, 1, 3, 1)
        grid.addWidget(mph, 5, 2, 3, 2)
        grid.addWidget(carStats, 5, 4, 3, 1)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ex = MyMainWindow()
    sys.exit(app.exec_())