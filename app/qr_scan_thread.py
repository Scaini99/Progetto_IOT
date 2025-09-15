import threading
from queue import Queue

from custom_lib.conveyoryeeter.watchmypack import WatchMyPack
import constants


def qr_reader(queue: Queue, stop_event: threading.Event, database):

    camera = WatchMyPack(camera_id=0)
    prev_id= None

    while not stop_event.is_set():
        current_id= camera.read_qr_code()

        if current_id and current_id != prev_id:
            prev_id= current_id
            print("QR Code rilevato:", current_id)

            cur = database.cursor()
            cur.execute("SELECT veicolo_assegnato FROM consegna WHERE numero_ordine = %s", (current_id,))
        
            result = cur.fetchone()
            vehicle_id = result[0] ## 'id sia lo stesso della bay
            loading_bay= result[0]

            print(f"pacco: {current_id}\nveicolo: {vehicle_id}\nloading bay: {loading_bay}")

            message = (current_id, vehicle_id, loading_bay)
            queue.put(message)