import RPi.GPIO as GPIO
import time

# PIN
TRIG = 23
ECHO = 24

# PARAMETRI
SOGLIA_CM = 20      # distanza sotto cui consideri "oggetto presente"
INTERVALLO = 0.1   # tempo tra le misure

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

time.sleep(2)

def misura_distanza():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    timeout = start_time + 0.04  # 40 ms timeout

    while GPIO.input(ECHO) == 0:
        if time.time() > timeout:
            return None
        start = time.time()

    while GPIO.input(ECHO) == 1:
        if time.time() > timeout:
            return None
        stop = time.time()

    durata = stop - start
    distanza = (durata * 34300) / 2
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
            # QUI mandi il segnale al Raspberry
            # es: GPIO.output(PIN, True) / salva file / manda MQTT ecc.
            oggetto_presente = True

        # OGGETTO ESCE
        elif distanza >= SOGLIA_CM and oggetto_presente:
            print("Oggetto rimosso")
            oggetto_presente = False

        time.sleep(INTERVALLO)

except KeyboardInterrupt:
    GPIO.cleanup()
