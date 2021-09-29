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
import time
import numpy as np
import pyqtgraph as pg
from datetime import datetime
from pathlib import Path

class Waveforms(QObject):

    signal_plot1 = Signal(np.ndarray,np.ndarray)
    signal_plot2 = Signal(np.ndarray,np.ndarray)
    signal_plot3 = Signal(np.ndarray,np.ndarray)

    signal_readings = Signal(np.ndarray)
    signal_plots = Signal(np.ndarray,np.ndarray)

    def __init__(self,microcontroller):
        QObject.__init__(self)
        self.file = open(str(Path.home()) + "/Downloads/" + datetime.now().strftime('%Y-%m-%d %H-%M-%-S.%f') + ".csv", "w+")
        # self.file.write('Time (s),Paw (cmH2O),Flow (l/min),Volume (ml),Vt (ml),Ti (s),RR (/min),PEEP (cmH2O)\n')
        self.microcontroller = microcontroller

        self.time = 0
        self.time_array = np.array([])

        self.ch = {}
        for i in range(NUMBER_OF_CHANNELS):
            self.ch[str(i)] = 0

        self.temperature = {}
        for i in range(NUMBER_OF_CHANNELS):
            self.temperature[str(i)] = 0

        self.ch_array = {}
        for i in range(NUMBER_OF_CHANNELS):
            self.ch_array[str(i)] = np.array([])

        self.temperature_array = {}
        for i in range(NUMBER_OF_CHANNELS):
            self.temperature_array[str(i)] = np.array([])

        self.timer_update_waveform = QTimer()
        self.timer_update_waveform.setInterval(MCU.DATA_INTERVAL_ms/2)
        self.timer_update_waveform.timeout.connect(self.update_waveforms)
        self.timer_update_waveform.start()

        self.first_run = True
        self.time_ticks_start = 0

        self.time_now = 0
        self.time_diff = 0
        self.time_prev = time.time()

        self.counter_display = 0
        self.counter_file_flush = 0

        self.logging_is_on = True

    def logging_onoff(self,state,experimentID):
        self.logging_is_on = state
        if state == False:
            self.file.close()
        else:
            self.experimentID = experimentID
            self.file = open(str(Path.home()) + "/Downloads/" + self.experimentID + '_' + datetime.now().strftime('%Y-%m-%d %H-%M-%-S.%f') + ".csv", "w+")

    def update_waveforms(self):
      
        if SIMULATION:
            # test plotting multiple data points at a time
            '''
            t_chunck = np.array([])
            ch1_chunck = np.array([])
            ch2_chunck = np.array([])
            ch3_chunck = np.array([])

            for i in range(MCU.TIMEPOINT_PER_UPDATE):
                self.time = time.time()
                self.ch1 = (self.ch1 + 0.2/MCU.TIMEPOINT_PER_UPDATE)%5
                self.ch2 = (self.ch2 + 0.1/MCU.TIMEPOINT_PER_UPDATE)%5
                self.ch3 = 0

                # append variables for plotting
                t_chunck = np.append(t_chunck,self.time)
                ch1_chunck = np.append(ch1_chunck,self.ch1)
                ch2_chunck = np.append(ch2_chunck,self.ch2)
                ch3_chunck = np.append(ch3_chunck,self.ch3)

            self.time_array = np.append(self.time_array,t_chunck)
            self.ch1_array = np.append(self.ch1_array,ch1_chunck)
            self.ch2_array = np.append(self.ch2_array,ch2_chunck)
            self.ch3_array = np.append(self.ch3_array,ch2_chunck)

            self.signal_plot1.emit(self.time_array,self.ch1_array)
            self.signal_plot2.emit(self.time_array,self.ch2_array)
            self.signal_plot3.emit(self.time_array,self.ch3_array)

            self.signal_readings['1'].emit("{:.2f}".format(self.ch1))
            self.signal_readings['2'].emit("{:.2f}".format(self.ch2))
            self.signal_readings['3'].emit("{:.2f}".format(self.ch3))
            '''
        else:
            readout = self.microcontroller.read_received_packet_nowait()
            if readout is not None:

                self.time_now = time.time()

                # chunck of measurements, n = TIMEPOINT_PER_UPDATE
                t_chunck = np.array([])
                ch_chunck = {}
                for k in range(NUMBER_OF_CHANNELS):
                    ch_chunck[str(k)] = np.array([])
                temperature_chunck = {}
                for k in range(NUMBER_OF_CHANNELS):
                    temperature_chunck[str(k)] = np.array([])

                for i in range(MCU.TIMEPOINT_PER_UPDATE):
                    # time
                    self.time_ticks = int.from_bytes(readout[i*MCU.RECORD_LENGTH_BYTE:i*MCU.RECORD_LENGTH_BYTE+4], byteorder='big', signed=False)
                    if self.first_run:
                        self.time_ticks_start = self.time_ticks
                        self.first_run = False
                    self.time = (self.time_ticks - self.time_ticks_start)*MCU.TIMER_PERIOD_ms/1000

                    # channel readings
                    for k in range(NUMBER_OF_CHANNELS):
                        self.ch[str(k)] = utils.unsigned_to_unsigned(readout[i*MCU.RECORD_LENGTH_BYTE+4+k*2:i*MCU.RECORD_LENGTH_BYTE+6+k*2],2)
                        ch_chunck[str(k)] = np.append(ch_chunck[str(k)],self.ch[str(k)])

                    # calculate temperature
                    for k in range(NUMBER_OF_CHANNELS-1):
                        self.temperature[str(k)] = utils.DACs_to_temp(self.ch[str(NUMBER_OF_CHANNELS-1)],self.ch[str(k)],100000)
                        temperature_chunck[str(k)] = np.append(temperature_chunck[str(k)],self.temperature[str(k)])

                    # line to write
                    record_from_MCU = str(self.time_ticks) + '\t'
                    for k in range(NUMBER_OF_CHANNELS):
                        record_from_MCU = record_from_MCU + str(self.ch[str(k)]) + '\t'
                    for k in range(NUMBER_OF_CHANNELS-1):
                        record_from_MCU = record_from_MCU + str(self.temperature[str(k)]) + '\t'
                    record_settings = (str(self.time_now))
                   
                    # saved variables
                    if self.logging_is_on:
                        self.file.write(record_from_MCU + record_settings + '\n')

                    # append variables for plotting
                    t_chunck = np.append(t_chunck,self.time)

                self.time_array = np.append(self.time_array,t_chunck)
                for k in range(NUMBER_OF_CHANNELS):
                    self.ch_array[str(k)] = np.append(self.ch_array[str(k)],ch_chunck[str(k)])
                for k in range(NUMBER_OF_CHANNELS-1):
                    self.temperature_array[str(k)] = np.append(self.temperature_array[str(k)],temperature_chunck[str(k)])

                # emit signals with reduced display refresh rate
                self.counter_display = self.counter_display + 1
                if self.counter_display>=1:
                    self.counter_display = 0
                    # emit plots
                    if PLOT_TEMPERATURE:
                        plot_arrays = self.temperature_array[str(0)]
                        for k in range(1,NUMBER_OF_CHANNELS_DISPLAY):
                            plot_arrays = np.vstack((plot_arrays,self.temperature_array[str(k)]))
                        self.signal_plots.emit(self.time_array,plot_arrays)
                        # emit readings
                        readings_to_display = np.array([])
                        for k in range(NUMBER_OF_CHANNELS_DISPLAY):
                            readings_to_display = np.append(readings_to_display,self.temperature[str(k)])
                        self.signal_readings.emit(readings_to_display)
                    else:
                        plot_arrays = self.ch_array[str(0)]
                        for k in range(1,NUMBER_OF_CHANNELS_DISPLAY):
                            plot_arrays = np.vstack((plot_arrays,self.ch_array[str(k)]))
                        self.signal_plots.emit(self.time_array,plot_arrays)
                        # emit readings
                        readings_to_display = np.array([])
                        for k in range(NUMBER_OF_CHANNELS_DISPLAY):
                            readings_to_display = np.append(readings_to_display,self.ch[str(k)])
                        self.signal_readings.emit(readings_to_display)

        # file flushing
        if self.logging_is_on:
            self.counter_file_flush = self.counter_file_flush + 1
            if self.counter_file_flush>=500:
                self.counter_file_flush = 0
                self.file.flush()

    def close(self):
        self.file.close()