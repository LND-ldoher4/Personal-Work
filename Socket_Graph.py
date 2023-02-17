from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QVBoxLayout, QLabel, QFontDialog
from PyQt5 import QtWidgets, QtCore, uic
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import sys  
from random import randint
import numpy as np

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,  *args, **kwargs):
        super(MainWindow,self).__init__( *args, **kwargs)
        uic.loadUi('C:/Users/Liam Doherty/Documents/UIC_UR/UIC_UR_programs/SocketCode/Pressure_Graphing.ui', self)
        #vvv---------------------------------------starting values---------------------------------------vvv#
        self.x = list(range(1))  # starts the graph time at zero
        self.y = [0 for _ in range(1)]  
        self.out = [0 for _ in range(1)]  
        self.sy = [0 for _ in range(1)]
        self.sz = [0 for _ in range(1)]
        #---------------------------------------------------------------------------------------------------#
        #vvv----------------------------------------graph set up-----------------------------------------vvv#
        pen_g=pg.mkPen(0,250,0)
        pen_r=pg.mkPen(250,0,0)
        pen_out=pg.mkPen(color='grey')
        self.GLine=self.GLineWidget.plot(self.x,self.y, pen=pen_g)
        self.gScat = self.ScatterWidget.scatterPlot(self.x,self.sy, pen=pen_g, symbol= 'o', symbolSize = 19,symbolBrush='green')
        self.rScat = self.ScatterWidget.scatterPlot(self.x,self.sz, pen=pen_r, symbol= 'o', symbolSize = 19,symbolBrush='red')
        self.outScat = self.ScatterWidget.scatterPlot(self.out,self.sz, pen=pen_out, symbol= 's', symbolSize=20, symbolBrush='grey')
        self.GLineWidget.setYRange(0,100)
        self.GLineWidget.setBackground('w')
        self.ScatterWidget.setBackground('w')
        self.GLineWidget.setLabel('left', "<span style=\"color:black;font-size:15px\"># of green </span>")
        self.GLineWidget.setLabel('bottom', "<span style=\"color:black;font-size:15px\">Second (sec)</span>")
        self.ScatterWidget.setLabel('left', "<span style=\"color:black;font-size:15px\"></span>")
        self.ScatterWidget.setLabel('bottom', "<span style=\"color:black;font-size:15px\"> </span>")
        #---------------------------------------------------------------------------------------------------#
        #vvv--------------------------------------the slider code----------------------------------------vvv#
        self.t=500 #this is needed to make sure that the threshold starts at the right position and is called later in the code
        self.ThresholdSlider.valueChanged[int].connect(self.changeValue) #tells what happens when the slider is moved       
    def changeValue(self, value): 
        self.t = int(value)
        #---------------------------------------------------------------------------------------------------#
        #vvv--------------------------------------Updata Plot Data---------------------------------------vvv#
    def update_plot_data(self,press_data):
        self.x.append(self.x[-1] + 1)# Increase x range by 1 point every second
        y_new = press_data
        greens = np.where(y_new >= self.t)
        out= np.where(y_new < 2)
        y_new=np.where(y_new >= 2, y_new, 500)
        reds = np.where( y_new < self.t)
        #out= np.where(y_new == 1)
        self.y.append( len(greens[1]))  # Add a new random value as place holder, how will the data be input (see line 14)
        self.GLine.setData(self.x, self.y) #fully updates line plot
        # rows
        self.gScat.setData(greens[0], greens[1]) #fully updates scatter plot
        self.rScat.setData(reds[0], reds[1])
        self.outScat.setData(out[0], out[1])
        #---------------------------------------------------------------------------------------------------#