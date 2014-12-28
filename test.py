from multiprocessing import Process, Pipe
#Basic imports
from ctypes import *
import sys
#Phidget specific imports
from Phidgets.Phidget import Phidget
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AccelerationChangeEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.Accelerometer import Accelerometer


from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, CurrentChangeEventArgs, PositionChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.AdvancedServo import AdvancedServo
from Phidgets.Devices.Servo import ServoTypes

delta_pos = 0.05
#Create an accelerometer object
try:
    accelerometer = Accelerometer()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)
    
    
try:
    advancedServo = AdvancedServo()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)
    
    
try:
    advancedServo2 = AdvancedServo()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)    
#========================================================================================================================================================================================
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
        print("Phidget Exception %i: %s" % (e.code, e.details))

def AccelerometerAccelerationChanged(e):
    source = e.device
    accelerometer.pconn.send("%i:%6f" % (e.index, e.acceleration))

    
#========================================================================================================================================================================================

def f(conn):
#    conn.send([42, None, 'hello'])
    accelerometer.pconn = conn
    try:
        accelerometer.setOnAttachHandler(AccelerometerAttached)
        accelerometer.setOnDetachHandler(AccelerometerDetached)
        accelerometer.setOnErrorhandler(AccelerometerError)
        accelerometer.setOnAccelerationChangeHandler(AccelerometerAccelerationChanged)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    print("Opening phidget object....")

    try:
        accelerometer.openPhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    print("Waiting for attach....")

    try:
        accelerometer.waitForAttach(10000)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        try:
            accelerometer.closePhidget()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)
        print("Exiting....")
        exit(1)
    else:
        try:
            numAxis = accelerometer.getAxisCount()
            accelerometer.setAccelChangeTrigger(0, 0.02)
            accelerometer.setAccelChangeTrigger(1, 0.02)
            if numAxis > 2:
                accelerometer.setAccelChangeTrigger(2, 0.500)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
    
        DisplayDeviceInfo()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    f(child_conn)
    
#--------------------------------------------------------------------------------------------------------------------------------------
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
   
def M1_Init():

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
    
    
def M1_Start():
    try:
        advancedServo.setEngaged(0, True)
    except:
        print "Can't start M1"
        try:
            advancedServo.closePhidget()
            M1_Init()
        except:
            print "Can't reopen M1'"
            
    
def M1_Stop():
    try:
        advancedServo.setEngaged(0, False)   
    except:
        print "Can't stop M1"

def M1_Rotate(pos):
        if cmd[0:1] == '1':
            try:
                pos=float(cmd[2:])
                if (abs(pos) > delta_pos):
                    if pos>0:
                        advancedServo.setPosition(0, advancedServo.getPosition(0)-1) #
                    else:
                        advancedServo.setPosition(0, advancedServo.getPosition(0)+1) #
            except Exception as e:
                print("M1 Exception %i: %s" % (e.code, e.details))
                
def M1_Close():
    advancedServo.closePhidget()
#---------------------------------------------------------------------------------------------------------------------------------------------------
def M2_Attached(e):
    attached = e.device
    print("Servo %i Attached!" % (attached.getSerialNum()))

def M2_Detached(e):
    detached = e.device
    print("Servo %i Detached!" % (detached.getSerialNum()))


    
def M2_Error(e):
    try:
        source = e.device
        print("Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        advancedServo2.closePhidget()
   
def M2_Init():

    try:
        advancedServo2.openPhidget(119567)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
            
    try:
        advancedServo2.waitForAttach(10000)
    except PhidgetException as e:
        print("Exception %i: %s " % (e.code, e.details))
        try:
            advancedServo2.closePhidget()
        except PhidgetException as e:
            print("Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)
        print("Error advancedServo.waitForAttach....")
    
    try:
        advancedServo2.setOnAttachHandler(M2_Attached)
        advancedServo2.setOnDetachHandler(M2_Detached)
        advancedServo2.setOnErrorhandler(M2_Error)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
    
    advancedServo2.setServoType(0, ServoTypes.PHIDGET_SERVO_DEFAULT)
    advancedServo2.setVelocityLimit(0, advancedServo2.getVelocityMax(0))
    advancedServo2.setAcceleration(0, advancedServo2.getAccelerationMax(0))
    
    
def M2_Start():
    advancedServo2.setEngaged(0, True)
           
    
def M2_Stop():
        advancedServo2.setEngaged(0, False)   

def M2_Rotate(cmd):
        if cmd[0:1] == '0':
            try:
                pos=float(cmd[2:])
                if (abs(pos) > delta_pos):
                    if pos>0:
                        advancedServo2.setPosition(0, advancedServo2.getPosition(0)-1) #
                    else:
                        advancedServo2.setPosition(0, advancedServo2.getPosition(0)+1) #
            except Exception as e:
                print("M2 Exception %i: %s" % (e.code, e.details))
    
def M2_Close():
    advancedServo2.closePhidget()

#---------------------------------------------------------------------------------------------------------------------------------------------------
M1_Init()
M1_Start()

M2_Init()
M2_Start()
#----------------------------------------------------------------------------------------------------------------------------------------------------    

while(True):
        cmd = parent_conn.recv()
        M1_Rotate(cmd)
        M2_Rotate(cmd)

