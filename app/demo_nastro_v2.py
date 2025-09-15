import cv2
import threading
import time
from queue import Queue, Empty
from pyzbar import pyzbar
import psycopg2
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
Device.pin_factory = PiGPIOFactory()


from custom_lib.conveyoryeeter.watchmypack import WatchMyPack
import constants

## thread 
from qr_scan_thread import qr_reader
from phisical_stations_thread import phisical_stations
from conveyor_thread import conveyor_belt


## Debug: printa il msg che dovrebbe smistare i pacchi
## phisical_station testuale
def qr_printer(queue: Queue, stop_event: threading.Event):
    while not stop_event.is_set():
        try:
            message = queue.get(timeout=0.5)
        except Empty:
            continue
        else:
            print(f"inserimento pacco in loading bay {message[2]}")

def main():
    database = psycopg2.connect( 
                            host=constants.DBHOST,
                            port=constants.DBPORT,
                            database=constants.DBNAME,
                            user= constants.DBUSER,
                            password= constants.DBPASSWORD
                           )
    try:
        database
        print("Connessione database attiva")
    except NameError:
        print("Connessione database non avvenuta")
    
    
    
    ## coda di pacchi scannerizzati:
    ## elementi: (current_id, vehicle_id, loading_bay)
    queue = Queue()
    conveyor_stop_event = threading.Event()
    stop_event = threading.Event()

    conveyor_thread = threading.Thread(target=conveyor_belt, args=(conveyor_stop_event,))
    reader_thread = threading.Thread(target=qr_reader, args=(queue, stop_event, database))
    printer_thread = threading.Thread(target=phisical_stations, args=(queue, stop_event))
     
    conveyor_thread.start()
    reader_thread.start()
    printer_thread.start()

    print("dormo 5 sec")
    time.sleep(5)
    conveyor_stop_event.set()
    
    ##conveyor_thread.join() 
    ##reader_thread.join()
    printer_thread.join()
    print("Terminato.")

if __name__ == "__main__":
    main()
