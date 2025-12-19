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
    
    cur= database.cursor()
    cur.execute("SELECT COUNT(*) AS totale_pacchi FROM consegna;")
    result= cur.fetchone()
    to_be_smisted= result[0]
    
    
    ## coda di pacchi scannerizzati:
    ## elementi: (current_id, vehicle_id, loading_bay)
    queue = Queue()
    reader_done_event = threading.Event()
    phisical_stations_done_event = threading.Event()

    conveyor_thread = threading.Thread(target=conveyor_belt, args=(
        reader_done_event, ## comunica la fine di qr_scan_thread
        phisical_stations_done_event ## comunica la fine di phisical_stations_thread
        ))

    qr_scan_thread = threading.Thread(target=qr_reader, args=(
        queue, ## canale qr_scan_thread - phisical_stations_thread
        reader_done_event, ## comunica la sua fine
        database, ## connessione al db
        to_be_smisted ## pacchi da smistare in giornata
        ))

    phisical_stations_thread = threading.Thread(target=phisical_stations, args=(
        queue, ## canale qr_scan_thread - phisical_stations_thread
        phisical_stations_done_event, ## comunica la sua fine
        to_be_smisted ## pacchi da smistare in giornata
        ))
     
    conveyor_thread.start()
    qr_scan_thread.start()
    phisical_stations_thread.start()


    print("Working hard for you...")

if __name__ == "__main__":
    main()
