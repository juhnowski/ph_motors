from multiprocessing import Process, Pipe
#Basic imports
from ctypes import *
import sys
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit

from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, CurrentChangeEventArgs, PositionChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.AdvancedServo import AdvancedServo
from Phidgets.Devices.Servo import ServoTypes

delta_pos = 0.05
flag_m1 = True
flag_m2 = True
#Create an interfacekit object
try:
    interfaceKit = InterfaceKit()
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

def f():
#    interfaceKit.pconn = conn
    try:
        interfaceKit.setOnAttachHandler(inferfaceKitAttached)
        interfaceKit.setOnDetachHandler(interfaceKitDetached)
        interfaceKit.setOnErrorhandler(interfaceKitError)
        interfaceKit.setOnInputChangeHandler(interfaceKitInputChanged)
        interfaceKit.setOnOutputChangeHandler(interfaceKitOutputChanged)
        interfaceKit.setOnSensorChangeHandler(interfaceKitSensorChanged)
    except PhidgetException as e:
        print("Interface Kit Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    print("Opening Interface Kit....")

    try:
        interfaceKit.openPhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    print("Waiting for Interface Kit attach....")

    try:
        interfaceKit.waitForAttach(10000)
    except PhidgetException as e:
        print("Interface Kit Exception %i: %s" % (e.code, e.details))
        try:
            interfaceKit.closePhidget()
        except PhidgetException as e:
            print("Interface Kit Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)
        print("Exiting....")
        exit(1)
    else:
        displayDeviceInfo()

    print("Interface Kit: Setting the data rate for each sensor index to 4ms....")
    for i in range(interfaceKit.getSensorCount()):
        try:
            interfaceKit.setDataRate(i, 100)
        except PhidgetException as e:
            print("Interface Kit Exception %i: %s" % (e.code, e.details))
    
#--------------------------------------------------------------------------------------------------------------------------------------
def M1_Attached(e):
    attached = e.device
    print("Servo %i Attached!" % (attached.getSerialNum()))

def M1_Detached(e):
    detached = e.device
    print("M1 Servo %i Detached!" % (detached.getSerialNum()))
    exit(1)

    
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
#        if cmd[0:1] == '1':
#            pos=int(cmd[2:])
            pos = pos*180/999 
            advancedServo.setPosition(0, pos)
            flag_m1 = True
                
def M1_Close():
    advancedServo.closePhidget()
#---------------------------------------------------------------------------------------------------------------------------------------------------
def M2_Attached(e):
    attached = e.device
    print("Servo %i Attached!" % (attached.getSerialNum()))

def M2_Detached(e):
    detached = e.device
    print("M2 Servo %i Detached!" % (detached.getSerialNum()))
    exit(1)

    
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

def M2_Rotate(pos):
#        if cmd[0:1] == '0':
#                pos=int(cmd[2:])
                pos = pos*180/999 
                advancedServo2.setPosition(0, pos)
                flag_m2 = True
    
def M2_Close():
    advancedServo2.closePhidget()


#========================================================================================================================================================================================
#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (interfaceKit.isAttached(), interfaceKit.getDeviceName(), interfaceKit.getSerialNum(), interfaceKit.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Digital Inputs: %i" % (interfaceKit.getInputCount()))
    print("Number of Digital Outputs: %i" % (interfaceKit.getOutputCount()))
    print("Number of Sensor Inputs: %i" % (interfaceKit.getSensorCount()))

#Event Handler Callback Functions
def inferfaceKitAttached(e):
    attached = e.device
    print("InterfaceKit %i Attached!" % (attached.getSerialNum()))

def interfaceKitDetached(e):
    detached = e.device
    print("InterfaceKit %i Detached!" % (detached.getSerialNum()))

def interfaceKitError(e):
    try:
        source = e.device
        print("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def interfaceKitInputChanged(e):
    source = e.device
    print("InterfaceKit %i: Input %i: %s" % (source.getSerialNum(), e.index, e.state))

def interfaceKitSensorChanged(e):
    source = e.device
    #print("%i:%i" % (e.index, e.value))
    #interfaceKit.pconn.send("%i:%i" % (e.index, e.value))
    if e.index == 0:
        if flag_m2:
            flag_m2 = False
            M2_Rotate(e.value)
    else:
        if flag_m1:
            flag_m1 = False
            M1_Rotate(e.value)
            

def interfaceKitOutputChanged(e):
    source = e.device
    print("InterfaceKit %i: Output %i: %s" % (source.getSerialNum(), e.index, e.state))



    
#========================================================================================================================================================================================


#---------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    print("M1_Init start")
    M1_Init()
    print("M1_Init done")
    print("M1_Start start")        
    M1_Start()
    print("M1_Start done")        
    
    print("M2_Init start")
    M2_Init()
    print("M2_Init done")
    print("M2_Start start")        
    M2_Start()
    print("M2_Start done")        
    print("f start")        
    f()
    print("f done")


    while(True):
        cmd = parent_conn.recv()
        print("cmd=%s"%cmd)
        M1_Rotate(cmd)
        M2_Rotate(cmd)
