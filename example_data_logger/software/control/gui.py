# set QT_API environment variable
import os 
os.environ["QT_API"] = "pyqt5"
import qtpy
import argparse

# qt libraries
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *

# app specific libraries
import control.widgets as widgets
import control.core as core
import control.microcontroller as microcontroller
from control._def import *

parser = argparse.ArgumentParser()
parser.add_argument("--simulation", help="Run the GUI with simulated image streams.", action = 'store_true')
args = parser.parse_args()

class VentDevGUI(QMainWindow):

	# variables
	fps_software_trigger = 100

	def __init__(self, is_simulation = False, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# load objects
		if is_simulation:
			self.microcontroller = microcontroller.Microcontroller_Simulation()
		else:
			self.microcontroller = microcontroller.Microcontroller()
		self.waveforms = core.Waveforms(self.microcontroller)
		
		# load widgets
		self.waveformDisplay = widgets.WaveformDisplay()
		self.controlPanel = widgets.ControlPanel()

		# layout widgets
		layout = QGridLayout() #layout = QStackedLayout()
		layout.addWidget(self.waveformDisplay,0,0)
		layout.addWidget(self.controlPanel,1,0)

		# transfer the layout to the central widget
		self.centralWidget = QWidget()
		self.centralWidget.setLayout(layout)
		self.setCentralWidget(self.centralWidget)

		# make connections
		self.controlPanel.signal_logging_onoff.connect(self.waveforms.logging_onoff)
		self.waveforms.signal_plots.connect(self.waveformDisplay.plot)
		self.waveforms.signal_readings.connect(self.controlPanel.display_readings)

	def closeEvent(self, event):
		self.waveforms.close()
		event.accept()