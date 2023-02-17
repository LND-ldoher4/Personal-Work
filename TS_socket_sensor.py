import sys
from turtle import width
import clr
import sys
import getopt

import time
import pylsl
from pylsl import StreamInfo, StreamOutlet, local_clock
#vvv----------------- printFrame Definition --------------------vvv#
def printFrame( frameArray, sensorColumns):
        sensels=[]
        senselsNR=[]
        for i, sensel in enumerate(frameArray,1):
                FRMTsensel = sensel#str(sensel)
                if (i%sensorColumns)!=0:
                        senselsNR.append(FRMTsensel)
                else:
                        if(i>0):
                                senselsNR.append(FRMTsensel)
                                sensels.append(senselsNR)
                                senselsNR=[]
                        else:
                                senselsNR.append(FRMTsensel)
                                
        #print (sensels)
        return sensels
#------------------------------------------------------------------#
#vvv---------------Set up for the rest of the code--------------vvv#
sys.path.append(r"C:/Tekscan/TekAPI/x64")
clr.AddReference("TekAPI64")

from TekAPI import CTekAPI
pTekAPI = CTekAPI()
pTekAPI.TekSetMapFileDirectory(r"C:/Tekscan/TekAPI/Samples")
err=pTekAPI.TekGetLastError()
print(err)

pTekAPI.TekInitializeHardware()
print("Detecting sensor hardware...")

availableNumbers = []
err, availableSerialNumbers = pTekAPI.TekEnumerateHandles(availableNumbers)
print(err)
print(*availableSerialNumbers, sep='\n')
info = pylsl.StreamInfo('SocketSensor', 'EEG', 1, 100, 'float32', 'myuid2424')
srate=100
#------------------------------------------------------------------#
#vvv---- Sensor (de)activation/setting the operation details----vvv#
if (len(availableSerialNumbers) > 0):##Activiates the script when sensors are detected
        print("Good to Go! Initializing hardware...")
        
        mapFilePath=r"C:/Tekscan/TekAPI/9811.mp"##DO NOT CHANGE THIS FILE PATH
        framePeriod=10000 ##10000 microseconds = 100 Hz
        timeout=600##the time out in milliseconds. last we checked it cannot be less than 300
        frameData=bytearray()##how we want to format the data recieved from hardware
        columns=0

        prnt=pTekAPI.TekClaimSensor(availableSerialNumbers, mapFilePath)##claim the first sensor
        print(prnt)
        if (len(availableSerialNumbers)>1):
            err, availableSerialNumbers1 = pTekAPI.TekEnumerateHandles(availableNumbers)
            prnt=pTekAPI.TekClaimSensor(availableSerialNumbers1, mapFilePath)##claim the second sensor
            print(prnt)
        for i in availableSerialNumbers: 
            pTekAPI.TekInitializeSensor(i, framePeriod)##activate the nth sensor 
            pTekAPI.TekSetSensitivityLevel(i,40)##set sensitivity of the nth sensor
else:  ##Deactiviates the script when no sensors are detected
        print("Cannot detect sensors: Deinitializing hardware...")
        pTekAPI.TekDeinitializeHardware() 
        sys.exit()
#------------------------------------------------------------------#
#vvv---------------- produce results, hopefully ----------------vvv#
err, dataFrame0= pTekAPI.TekCaptureDataFrame(availableSerialNumbers[0],timeout,frameData)##we need this to make sure that the hardware actually connects
err, columns0 = pTekAPI.TekGetSensorColumns(availableSerialNumbers[0], columns)
if (len(availableSerialNumbers)>1):
    err, dataFrame1= pTekAPI.TekCaptureDataFrame(availableSerialNumbers[1],timeout,frameData)##we need this to make sure that the hardware actually connects
    err, columns1 = pTekAPI.TekGetSensorColumns(availableSerialNumbers[1], columns)

pTekAPI.TekEnableLogging("C:\Tekscan\TekAPI\TekScanLog.txt")##logs any and all issues that happen while the code is running

outlet = pylsl.StreamOutlet(info, 1260, 360) #info, chunk size, for buffer size 360 is max
start_time = local_clock()
sent_samples = 0
try:
    while True:
        elapsed_time = local_clock() - start_time
        required_samples = int(srate * elapsed_time) - sent_samples
        for sample_ix in range(required_samples):
                err,dataFrame0=pTekAPI.TekCaptureDataFrame(availableSerialNumbers[0],timeout,frameData)
                Arr1=printFrame(dataFrame0,columns0)
                print(Arr1)
                outlet.push_chunk(Arr1)
                if (len(availableSerialNumbers)>1):
                        err, dataFrame1= pTekAPI.TekCaptureDataFrame(availableSerialNumbers[1],timeout,frameData)
                        Arr2=printFrame(dataFrame1,columns1)
                        outlet.push_chunk(Arr2)
        sent_samples += required_samples
        ## now send it and wait for a bit before trying again.
        time.sleep(0.01)
        ##it might be nice to store the data as a 3D array
        ##print the results in a clear and meaningful way, check that we can print the code in a GUI

except KeyboardInterrupt:
    print("Disconnecting to the hardware...")
    pTekAPI.TekReleaseSensor(availableSerialNumbers[0])
    pTekAPI.TekReleaseSensor(availableSerialNumbers[1])
    pTekAPI.TekDeinitializeHardware() 
    print("Disconnected hardware: Exiting run...")
    sys.exit()

###NOTES:
#I want to make the code so that it automatically initializes the sensors and sets the sensitivity, etc.
#I am gonna want to print the results so that I can actually tell that it works
#I want to produce a GUI so that it shows my results and test my understanding of the code
#maybe change the printFrame definition as it becomes more relevant