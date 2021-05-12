# set QT_API environment variable
import os 
os.environ["QT_API"] = "pyqt5"
import qtpy

# qt libraries
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *

import control.utils as utils
from control._def import *

from queue import Queue
from threading import Thread, Lock
import time
import numpy as np
import pyqtgraph as pg
from datetime import datetime

class NavigationController(QObject):

    xPos = Signal(float)
    yPos = Signal(float)
    zPos = Signal(float)

    def __init__(self,microcontroller):
        QObject.__init__(self)
        self.microcontroller = microcontroller
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0
        self.timer_read_pos = QTimer()
        self.timer_read_pos.setInterval(PosUpdate.INTERVAL_MS)
        self.timer_read_pos.timeout.connect(self.update_pos)
        self.timer_read_pos.start()

    def move_x(self,delta_mm,v,a,ustepping):
        delta_usteps = delta_mm*FULLSTEPS_PER_MM*ustepping
        velocity = int((v/VELOCITY_MAX)*65535)
        acceleration = int((a/ACCELERATION_MAX)*65535)
        self.microcontroller.move_x(delta_usteps,velocity,acceleration,ustepping)
        self.x_pos = self.x_pos + delta_mm
        print('X: ' + str(self.x_pos))
        self.xPos.emit(self.x_pos)

    def cycle_x(self,delta_mm,v,a,ustepping):
        delta_usteps = delta_mm*FULLSTEPS_PER_MM*ustepping
        velocity = int((v/VELOCITY_MAX)*65535)
        acceleration = int((a/ACCELERATION_MAX)*65535)
        self.microcontroller.cycle_x(delta_usteps,velocity,acceleration,ustepping)
        self.x_pos = self.x_pos + delta_mm
        print('X: ' + str(self.x_pos))
        self.xPos.emit(self.x_pos)

    def move_y(self,delta_mm,v,a,ustepping):
        delta_usteps = delta_mm*FULLSTEPS_PER_MM*ustepping
        velocity = int((v/VELOCITY_MAX)*65535)
        acceleration = int((a/ACCELERATION_MAX)*65535)
        self.microcontroller.move_y(delta_usteps,velocity,acceleration,ustepping)
        self.y_pos = self.y_pos + delta_mm
        print('Y: ' + str(self.y_pos))
        self.yPos.emit(self.y_pos)

    def cycle_y(self,delta_mm,v,a,ustepping):
        delta_usteps = delta_mm*FULLSTEPS_PER_MM*ustepping
        velocity = int((v/VELOCITY_MAX)*65535)
        acceleration = int((a/ACCELERATION_MAX)*65535)
        self.microcontroller.cycle_y(delta_usteps,velocity,acceleration,ustepping)

    def move_z(self,delta_mm,v,a,ustepping):
        delta_usteps = delta_mm*100*ustepping
        velocity = int((v/VELOCITY_MAX)*65535)
        acceleration = int((a/ACCELERATION_MAX)*65535)
        self.microcontroller.move_z(delta_usteps,velocity,acceleration,ustepping)
        self.z_pos = self.z_pos + delta_mm
        print('Z: ' + str(self.z_pos))
        self.zPos.emit(self.z_pos)

    def cycle_z(self,delta_mm,v,a,ustepping):
        delta_usteps = delta_mm*100*ustepping
        velocity = int((v/VELOCITY_MAX)*65535)
        acceleration = int((a/ACCELERATION_MAX)*65535)
        self.microcontroller.cycle_z(delta_usteps,velocity,acceleration,ustepping)

    def update_pos(self):
        pos = self.microcontroller.read_received_packet_nowait()
        if pos is None:
            return
        self.x_pos = utils.unsigned_to_signed(pos[0:3],MicrocontrollerDef.N_BYTES_POS)/Motion.STEPS_PER_MM_XY # @@@TODO@@@: move to microcontroller?
        self.y_pos = utils.unsigned_to_signed(pos[3:6],MicrocontrollerDef.N_BYTES_POS)/Motion.STEPS_PER_MM_XY # @@@TODO@@@: move to microcontroller?
        self.z_pos = utils.unsigned_to_signed(pos[6:9],MicrocontrollerDef.N_BYTES_POS)/Motion.STEPS_PER_MM_Z  # @@@TODO@@@: move to microcontroller?
        self.xPos.emit(self.x_pos)
        self.yPos.emit(self.y_pos)
        self.zPos.emit(self.z_pos*1000)

    def home(self):
        self.microcontroller.move_x(-self.x_pos)
        self.microcontroller.move_y(-self.y_pos)
