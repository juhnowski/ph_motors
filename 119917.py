from ctypes import *
import sys
from time import sleep
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, CurrentChangeEventArgs, PositionChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.AdvancedServo import AdvancedServo
from Phidgets.Devices.Servo import ServoTypes
from multiprocessing import Process, Pipe

from Phidgets.Phidget import Phidget
from Phidgets.Events.Events import AccelerationChangeEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.Accelerometer import Accelerometer
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
a_conn, m1_conn = Pipe()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
try:
    advancedServo = AdvancedServo()
    print ("M1 attached-----------------------------------------------------------------")
except:
    print("Error!!!!!!!!!!!")
        
        
        
def M1_Attached(e):
    attached = e.device
    print("Servo %i Attached!" % (attached.getSerialNum()))

def M1_Detached(e):
    detached = e.device
    print("Servo %i Detached!" % (detached.getSerialNum()))


    
def M1_Error(e):
    try:
        source = e.device
        print("Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        advancedServo.closePhidget()
   
def Init():

    try:
        advancedServo.openPhidget(119917)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
            
    try:
        advancedServo.waitForAttach(10000)
    except PhidgetException as e:
        print("Exception %i: %s " % (e.code, e.details))
        try:
            advancedServo.closePhidget()
        except PhidgetException as e:
            print("Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)
        print("Error advancedServo.waitForAttach....")
    
    try:
        advancedServo.setOnAttachHandler(M1_Attached)
        advancedServo.setOnDetachHandler(M1_Detached)
        advancedServo.setOnErrorhandler(M1_Error)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
    
    advancedServo.setServoType(0, ServoTypes.PHIDGET_SERVO_HITEC_HS422)
    advancedServo.setVelocityLimit(0, advancedServo.getVelocityMax(0))
    advancedServo.setAcceleration(0, advancedServo.getAccelerationMax(0))
    
    
def Start():
    try:
        advancedServo.setEngaged(0, True)
    except:
        print "Can't start M1"
        try:
            advancedServo.closePhidget()
            Init()
        except:
            print "Can't reopen M1'"
            
    
def Stop():
    try:
        advancedServo.setEngaged(0, False)   
    except:
        print "Can't stop M1"

def Rotate(pos):
    if advancedServo.getEngaged(0):
        if pos>0:
            advancedServo.setPosition(0, advancedServo.getPosition(0)-1) #
        else:
            advancedServo.setPosition(0, advancedServo.getPosition(0)+1) #
    else:
        print "M1 getEngaged(0) = False"
        Start()
        print "Try Start M1"
        
    
def Close():
    advancedServo.closePhidget()

Init()
min_pos = advancedServo.getPositionMin(0)
max_pos = advancedServo.getPositionMax(0)
Start()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
def target_m1(m1_conn):
    while(True):
        cmd = m1_conn.recv()
        if cmd[0:4]=='stop':
            Stop()
        elif cmd[0:5] == 'start':
            Start()
        elif cmd[0:4] == 'init':
            Init()
        elif cmd[0:5] == 'close':
            Close()
        elif cmd[0:1] == '1':
            try:
                pos=float(cmd[2:])
                print(pos)
                Rotate(pos)
            except Exception as e:
                print("M1 Exception %i: %s" % (e.code, e.details))
                print "M1 Unknown command: %s"%cmd
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#Create an accelerometer object
try:
    accelerometer = Accelerometer()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def DisplayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (accelerometer.isAttached(), accelerometer.getDeviceName(), accelerometer.getSerialNum(), accelerometer.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Axes: %i" % (accelerometer.getAxisCount()))

#Event Handler Callback Functions
def AccelerometerAttached(e):
    attached = e.device
    print("Accelerometer %i Attached!" % (attached.getSerialNum()))

def AccelerometerDetached(e):
    detached = e.device
    print("Accelerometer %i Detached!" % (detached.getSerialNum()))

def AccelerometerError(e):
    try:
        source = e.device
        print("Accelerometer %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Accelerometer Phidget Exception %i: %s" % (e.code, e.details))

def AccelerometerAccelerationChanged(e):
    source = e.device
    a_conn.send("%i:%6f" % (e.index, e.acceleration))


#Main Program Code
try:
    accelerometer.setOnAttachHandler(AccelerometerAttached)
    accelerometer.setOnDetachHandler(AccelerometerDetached)
    accelerometer.setOnErrorhandler(AccelerometerError)
    accelerometer.setOnAccelerationChangeHandler(AccelerometerAccelerationChanged)
except PhidgetException as e:
    print("Accelerometer Phidget Exception %i: %s" % (e.code, e.details))


print("Opening Accelerometer phidget object....")

try:
    accelerometer.openPhidget()
except PhidgetException as e:
    print("Accelerometer Phidget Exception %i: %s" % (e.code, e.details))


print("Waiting Accelerometer for attach....")

try:
    accelerometer.waitForAttach(10000)
except PhidgetException as e:
#    print("Accelerometer Phidget Exception %i: %s" % (e.code, e.details))
#    try:
#        accelerometer.closePhidget()
#    except PhidgetException as e:
#        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Error accelerometer.waitForAttach(10000)....")

else:
    try:
        numAxis = accelerometer.getAxisCount()
        accelerometer.setAccelChangeTrigger(0, 0.0001)
        accelerometer.setAccelChangeTrigger(1, 0.0001)
        if numAxis > 2:
            accelerometer.setAccelChangeTrigger(2, 0.500)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
    
    DisplayDeviceInfo()

#=================================================================================================================================================================
cons_m1 = Process(target=target_m1,args=(m1_conn,))
cons_m1.daemon=True
cons_m1.start()

#=================================================================================================================================================================
print("Press Enter to quit....")

chr = sys.stdin.read(1)

#print("Closing...")

#try:
#    accelerometer.closePhidget()
#except PhidgetException as e:
#    print("Phidget Exception %i: %s" % (e.code, e.details))
#    print("Exiting....")
#    exit(1)

#print("Done.")
#exit(0)    
