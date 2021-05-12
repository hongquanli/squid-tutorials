# set QT_API environment variable
import os 
os.environ["QT_API"] = "pyqt5"
import qtpy

# qt libraries
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *

from control._def import *

class LEDControlWidget(QFrame):
    def __init__(self, microcontroller, main=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.microcontroller = microcontroller
        self.add_components()
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)

    def add_components(self):
        self.btn_led = QPushButton("ON/OFF")
        self.btn_led.setCheckable(True)
        self.btn_led.setChecked(False)
        self.btn_led.setDefault(False)
        
        grid_line0 = QGridLayout()
        grid_line0.addWidget(QLabel('LED'), 0,0)
        grid_line0.addWidget(self.btn_led, 0,1)

        self.grid = QGridLayout()
        self.grid.addLayout(grid_line0,0,0)
        self.setLayout(self.grid)
    
        self.btn_led.clicked.connect(self.set_LED_state)

    def set_LED_state(self,pressed):
        self.microcontroller.set_LED_state(pressed)