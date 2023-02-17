import csv
import os
from random import randint
import numpy as np
from datetime import datetime
from pylsl import StreamInfo, StreamInlet, resolve_bypred
from PyQt5 import QtWidgets, uic, QtCore
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys

    ##xxx===set up the GUI===xxx##
class ECGWindow(QtWidgets.QMainWindow):  
    def __init__(self):
        super(ECGWindow,self).__init__()
        uic.loadUi('D:\Python\ECG_GUI.ui', self)#call the GUI file in
        self.ECGPlot.setBackground('w')
        self.tm=[]
        self.vl=[]
        self.ECGPlt=self.ECGPlot.plot(self.tm,self.vl,pen=pg.mkPen(255, 0, 0))
        self.ECGPlot.setLabel('left', 'mV')
        self.ECGPlot.setLabel('bottom', 'time')
    ##xxx====================xxx##
    ##xxx===update plot stuff===xxx##
    def updateplot(self,time,value):
        self.tm.append(time)
        self.vl.append(value)
        self.ECGPlt.setData(self.tm,self.vl)#call the results into the plots
    ##xxx=======================xxx##

app = QtWidgets.QApplication(sys.argv)
w = ECGWindow()
while True:  

    stream=resolve_bypred("name='datagather'")#find the correct stream
    inlet=StreamInlet(stream)#stream inlet
    ECG_data,timestamps=inlet.pull_chunk()
    #vvv prepare/sort data vvv
    col1=ECG_data[:,0]
    col2=ECG_data[:,1]
    w.updateplot(col1,col2)
    
    def up():
        col1=inlet.pull_chunk()
        col2=inlet.pull_chunk()
        w.updateplot(col1,col2)
    timer = QtCore.QTimer()
    timer.timeout.connect(up)
    timer.start(1000)

    w.show()
    sys.exit(app.exec_())
