import sys

from gui import GUI
from canbus import CanBus
from light_controller import LightController
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    canbus = CanBus()
    canbus.start()
    
    light_controller = LightController()
    light_controller.start()
    
    app = QApplication(sys.argv)
    gui = GUI(canbus, light_controller)
    app.exec()

def quit(canbus, light_controller):
    canbus.stop()
    canbus.join()
    light_controller.stop()
    light_controller.join()
    sys.exit(0)