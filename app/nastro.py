import time
import RPi.GPIO as GPIO
import custom_lib.conveyoryeeter as conveyoryeeter
import constants

PIN_CONVEYOR = constants.PIN_CTRL_CONVEYOR_BELT  # sostituisci con il tuo pin BCM
RELAY_ON = GPIO.HIGH   # Cambia a GPIO.LOW se il tuo modulo è attivo LOW
RELAY_OFF = GPIO.LOW   # Inverti se necessario

def main():
    GPIO.setmode(GPIO.BCM)
    print("ora low")
    GPIO.setup(PIN_CONVEYOR, GPIO.OUT, initial= GPIO.HIGH)

    time.sleep(5)
    conveyorbelt_engine = conveyoryeeter.conveyorbeltengine.ConveyorBeltEngine(PIN_CONVEYOR)
    print("ora start")
    conveyorbelt_engine.start()

    time.sleep(5)
    print("ora low")
    conveyorbelt_engine.stop()

    GPIO.cleanup()

if __name__ == "__main__":
 main()
