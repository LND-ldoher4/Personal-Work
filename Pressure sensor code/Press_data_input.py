import numpy as np
from PyQt5.QtCore import Qt
#from PyQt5.QtWidgets import QFormLayout
from PyQt5 import QtWidgets, QtCore
import sys
from pylsl import StreamInlet, resolve_stream
#local imports
from press_graph2 import MainWindow
import TS_Pressure_Sensor_Code_test as snsr
#layout=QFormLayout()
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
##import RealTime_SDK_Pythor.py




def AnotherWindow(sample):
    sample2=sample
    w.app2=QtWidgets.QApplication(sys.argv)
    w=MainWindow()
    w.update_plot_data(sample2)

#VVV actual code VVV
#inlets=0
#print('looking for stream...')
#streams=resolve_stream('name','EEG')
#for i in range[0,len(streams)]:
#    if streams == "PressureSensor":
#        inlets=inlets+1
#        inlet= StreamInlet(streams[i])
#        sample,timestamp=inlet.pull_sample()
#        if inlets > 1:
#            w=AnotherWindow(sample)
#            w.show()
#        else:
#            w.update_plot_data(sample)

def new_data():
    ## VVV placeholder code VVV
    place_press_data = np.random.randint(0,1000, size=(21,58)) #21 columns, 58 rows
    place_press_data = snsr.please()
    w.update_plot_data(place_press_data)
    ##pressure data needs to stay the same definition, however the data generation will need to change to ensure that real data can be input  
    ## I think I should try to start getting ready to add the TEK code to here 
    ## ^^^ placeholder code ^^^

#vv== We might need to get rid of this code depending on how we set up the script for the SDK ==vv
w.timer= QtCore.QTimer()
w.timer.setInterval(1000)
w.timer.timeout.connect(new_data)
w.timer.start()
#^^== timer code ==^^

w.show()
app.exec()
#if __name__=='AnotherWindow':
#    w.app2.exec()
#sys.exit(app.exec_())
