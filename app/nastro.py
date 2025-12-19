import time
import RPi.GPIO as GPIO
import custom_lib.conveyoryeeter as conveyoryeeter

PIN_CONVEYOR = 21  # sostituisci con il tuo pin BCM
RELAY_ON = GPIO.HIGH   # Cambia a GPIO.LOW se il tuo modulo è attivo LOW
RELAY_OFF = GPIO.LOW   # Inverti se necessario

def main():
    GPIO.setmode(GPIO.BCM)
    print("ora low")
    GPIO.setup(21, GPIO.OUT, initial= GPIO.HIGH)

    time.sleep(5)
    conveyorbelt_engine = conveyoryeeter.conveyorbeltengine.ConveyorBeltEngine(21)
    print("ora start")
    conveyorbelt_engine.start()

    time.sleep(5)
    print("ora low")
    conveyorbelt_engine.stop()

    GPIO.cleanup()

if __name__ == "__main__":
 main()
