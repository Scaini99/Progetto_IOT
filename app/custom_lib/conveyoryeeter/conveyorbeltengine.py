import RPi.GPIO as GPIO
import time

class ConveyorBeltEngine:
    def __init__(self, pin_rele):
        self.pin_rele= pin_rele
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_rele, GPIO.OUT, initial=GPIO.HIGH)
        

    def start(self):
        print("conveyor start")
        GPIO.output(self.pin_rele, GPIO.LOW)
    
        

    def stop(self):
        print("conveyor stop")
        GPIO.output(self.pin_rele, GPIO.HIGH)
        