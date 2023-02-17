import csv
import os
import numpy as np
from pylsl import StreamInfo, StreamOutlet, local_clock
from datetime import datetime
##===filepathing script===##
exe='Rep_1_Data.csv'
now = datetime.now()
timenow = now.strftime('%H_%M_%S')
folder=str('\Data_'+timenow)
filepath=str(r'C:\Users\Vicon-OEM\Desktop\BITN_app')
filepath=str(filepath+folder) #this filepath will be nessecary in finding the correct file
print(filepath)#check to see if the file is the correct one
##========================##
##===find the file folder that will store the data===##
for root, dirs, files in os.walk(filepath): #find filepath doesnt exist then make new filepath  
    #if statement here to establish if the next for loop needs to happen
    for name in files:
        if name == exe:
            flpth=os.path.abspath(os.path.join(root, name))
            print(flpth)
        elif name != exe: 
            print("The file doesnt exist or has the wrong filename.")
##===================================================##
##===read the file data===##
fldata=csv.reader(open(flpth),delimiter=',')
array= np.array(list(fldata)).astype('float')

##========================##
##===lsl stuff===##
inf=StreamInfo('datagather','EEG',2,100,'float32','datagather1')
out=StreamOutlet(inf)
out.push_chunk(array)

##===================##
##===notes and operating information===##
#This file is meant to be run with the code called appendFile via lab streaming layer, this script also requires that the user
#will also run the program on the same computer as the ECG data generating program. 
#Preferably at the same time as the code is being genrated.