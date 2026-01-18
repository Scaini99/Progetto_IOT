"""
Thread che permette di ricavare un qr code da un pacco

- crea un istanza di una fotocamera (WatchMyPack)
- legge il qr code dei pacchi che passano davanti
- cerca il codice in magazzino
- lo inserisce in una coda perchè venga smistato dalle sorting station (in un altro thread)
"""

import threading
from queue import Queue

from custom_lib.conveyoryeeter.watchmypack import WatchMyPack
import constants
import time


def qr_reader(queue: Queue, done_event: threading.Event, database, to_be_smisted: int):
    print("qr_reader: START")

    camera = WatchMyPack(camera_id=0)
    prev_id= None

    internal_package_counter= 0
 
    while internal_package_counter < to_be_smisted:
        current_id= camera.read_qr_code()

        if current_id and current_id != prev_id:
            prev_id= current_id
            print("QR Code rilevato:", current_id)

            cur = database.cursor()
            cur.execute("SELECT veicolo_assegnato FROM consegna WHERE numero_ordine = %s", (current_id,))
        
            result = cur.fetchone()
            vehicle_id = result[0] # id lo stesso della bay
            loading_bay= result[0]

            internal_package_counter = internal_package_counter + 1 

            print(f"qr_scan_thread: pacco: {current_id}\nveicolo: {vehicle_id}\nloading bay: {loading_bay}")

            message = (current_id, vehicle_id, loading_bay)
            queue.put(message)

        time.sleep(0.01)
    
    done_event.set()