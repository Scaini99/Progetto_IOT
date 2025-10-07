import RPi.GPIO as GPIO
import time

class ConveyorBeltEngine:
    def __init__(self, pin_rele):
        self.pin_rele= pin_rele
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_rele, GPIO.OUT, initial= GPIO.LOW)

    def start(self):
        GPIO.output(self.pin_rele, GPIO.HIGH)
    
        

    def stop(self):
        GPIO.output(self.pin_rele, GPIO.LOW)
        