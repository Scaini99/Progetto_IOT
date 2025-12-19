## composta da un rilevatore ad infrasuoni/infrarossi per rilevare la presenza di un pacco davanti
## e da un attuatore per spingere il pacco

"""
COME FUNZIONA

Ogni stazione ha una posizione nella linea, un rilevatore, un servomotore e una coda di azioni
La coda di azioni contiene True o False. Quando il rilevatore rileva un pacco, la stazione controlla la testa
della lista delle azioni. Se è True attiva il servomotore per far cadere il pacco, se è false non fa nulla.
Comunque la testa della lista viene estratta.
La logica dietro la lista delle azioni è dare alla stazione delle istruzioni da seguire in base ai pacchi
che le transitano davanti.
Le azioni da eseguire vengono appese in coda volta per volta secondo la seguente regola:
Sono presenti m postazioni.
Un pacco deve finire nella posizione n di m (con n <= m), allora nelle code delle azioni:
    - dalla posizione 1 alla posizione n-1 verrà inserita un valore False (guarda il pacco e lascialo passare)
    - nella posizione n verrà inserito il valore True (spingi il pacco)
    - nelle postazioni n+1 ... m non verrà inserito alcun valore (il pacco non lo vedranno mais)

【=◈︿◈=】:A mio avviso, trattasi di metodo alquanto convoluto
La mia onesta reazione: ¯\_(ツ)_/¯. Si, questo commento da warnings su python....
"""

## questo accrocchio server per testare al di fuori di un rpi
import platform


import RPi.GPIO as GPIO
from gpiozero import Servo

## fine accrocchio

from time import sleep, time


class DiverterStation:

    def __init__(self, position: int, trig_pin, echo_pin, servo_pin):
        self.position= position
        self.trigger = trig_pin
        self.echo = echo_pin
        self.servo = Servo(servo_pin)
        self.action_queue= []

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def is_passing(self) -> bool:
        GPIO.output(self.trigger, False)
        sleep(0.05)

        GPIO.output(self.trigger, True)
        sleep(0.00001)
        GPIO.output(self.trigger, False)

        timeout = 0.02  # 20 ms

        start_wait = time()
        while GPIO.input(self.echo) == 0:
            if time() - start_wait > timeout:
                return False
        start = time()

        while GPIO.input(self.echo) == 1:
            if time() - start > timeout:
                return False
        stop = time()

        durata = stop - start
        distanza = (durata * 34300) / 2  # cm

        return 5 < distanza < 30


    ## Da tarare meglio il movimento...
    def push_package(self):
            print("PUSHING")

            self.servo.value= -1
            sleep(1)
            self.servo.value= 0.5
            sleep(1)
            self.servo.value= -1

    def enqueue(self, action):
        """Aggiunge in coda"""
        self.action_queue.append(action)

    def dequeue(self) -> bool:
        """
        Rimuove e restituisce l'elemento in testa, o None se vuota. 
        P.S. non deve essere mai vuota
        """
        if self.action_queue:
            return self.action_queue.pop(0)
        else:
            return None
    
    def queue_length(self) -> int:
        return len(self.action_queue)

    def queue_print(self):
        print(f"queue: {self.action_queue}")