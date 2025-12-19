import RPi.GPIO as GPIO
import time

# PIN
TRIG = 23
ECHO = 24

# PARAMETRI
SOGLIA_CM = 20      # distanza sotto cui consideri "oggetto presente"
INTERVALLO = 0.1    # tempo tra le misure

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # disabilita warning di pin già usati
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

time.sleep(2)

def misura_distanza():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    timeout = 0.04  # 40 ms timeout
    start_time = time.time()

    start = None
    stop = None

    # Aspetto che ECHO diventi HIGH
    while GPIO.input(ECHO) == 0:
        if time.time() - start_time > timeout:
            return None
    start = time.time()

    # Aspetto che ECHO torni LOW
    while GPIO.input(ECHO) == 1:
        if time.time() - start > timeout:
            return None
    stop = time.time()

    durata = stop - start
    distanza = (durata * 34300) / 2  # cm
    return distanza

oggetto_presente = False

try:
    while True:
        distanza = misura_distanza()

        if distanza is None:
            continue

        # OGGETTO ENTRA
        if distanza < SOGLIA_CM and not oggetto_presente:
            print("OGGETTO RILEVATO")
            oggetto_presente = True

        # OGGETTO ESCE
        elif distanza >= SOGLIA_CM and oggetto_presente:
            print("Oggetto rimosso")
            oggetto_presente = False

        time.sleep(INTERVALLO)

except KeyboardInterrupt:
    GPIO.cleanup()
