import numpy as np
from PyQt5.QtCore import Qt
#from PyQt5.QtWidgets import QFormLayout
from PyQt5 import QtWidgets, QtCore
import sys
from pylsl import StreamInlet, resolve_stream
#local imports
from Socket_Graph import MainWindow
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
import random as rn


def AnotherWindow(sample):
    sample2=sample
    w.app2=QtWidgets.QApplication(sys.argv)
    w=MainWindow()
    w.update_plot_data(sample2)


#VVV actual code VVV
#inlets=0
#print('looking for stream...')
#streams=resolve_stream('name','EEG')
def new_data():
#    for i in range[0,len(streams)]:
#        if streams == "SocketSensor":
#            inlets=inlets+1
#            inlet= StreamInlet(streams[i])
#           sample,timestamp=inlet.pull_sample()
#            if inlets > 1:
#                w=AnotherWindow(sample)
#                w.show()
#            else:
#                w.update_plot_data(sample)
    ## VVV placeholder code VVV
    place_press_data = np.random.randint(0,1000, size=(6,16)) #21 columns, 58 rows
    place_press_data= np.array([[1,1,1,10,rn.randint(10, 1000),10,10,1,1],[1,1,10,10,rn.randint(10, 1000),rn.randint(10, 1000),rn.randint(10, 1000),10,1],[1,10,10,rn.randint(10, 1000),rn.randint(10, 1000),rn.randint(10, 1000),rn.randint(10, 1000),10,1],[1,10,10,rn.randint(10, 1000),rn.randint(10, 1000),rn.randint(10, 1000),rn.randint(10, 1000),10,1],[1,10,10,rn.randint(10, 1000),rn.randint(10, 1000),rn.randint(10, 1000),10,10,1],[1,10,10,rn.randint(10, 1000),rn.randint(10, 1000),rn.randint(10, 1000),10,1,1],[1,1,10,rn.randint(10, 1000),rn.randint(10, 1000),rn.randint(10, 1000),10,1,1],[1,1,10,rn.randint(10, 1000),rn.randint(10, 1000),10,10,1,1],[1,1,10,10,rn.randint(10, 1000),10,10,1,1],[1,1,1,10,rn.randint(10, 1000),10,1,1,1]])
    w.update_plot_data(np.rot90(place_press_data, k=3, axes=(0, 1)))
    ## ^^^ placeholder code ^^^

    
#vv================vv
w.timer= QtCore.QTimer()
w.timer.setInterval(1000)
w.timer.timeout.connect(new_data)
w.timer.start()
#^^== timer code ==^^

w.show()
app.exec()
