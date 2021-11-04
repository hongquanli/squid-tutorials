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
import control.gui as gui

parser = argparse.ArgumentParser()
parser.add_argument("--simulation", help="Run the GUI with simulated image streams.", action = 'store_true')
args = parser.parse_args()

if __name__ == "__main__":

    app = QApplication([])
    if args.simulation:
        win = gui.VentDevGUI(is_simulation=True)
    else:
        win = gui.VentDevGUI()
    win.show()
    app.exec_() #sys.exit(app.exec_())
