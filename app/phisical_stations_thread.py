"""
Thread di gestione delle postazioni 'sorting station': rilevano e spingono il carico verso la baia di carico corretta.

- crea sorting_station
- controlla una coda di pacchi scannerizzati
- inserisce il pacco nella coda della sorting station corretta
TODO
- per ogni stazione controlla se passa un pacco davanti
- se necessario devia il pacco

"""
from queue import Queue
import threading
import custom_lib.conveyoryeeter as conveyoryeeter  # nastro trasportatore
import constants


def phisical_stations(queue: Queue, stop_event: threading.Event):
    nr_postazioni= constants.NR_OF_VEHICLES


    ## inizializzazione postazioni (position, trigger, echo, servo)
    
    sorting_stations= []
    sorting_stations.append(conveyoryeeter.sortingstation.Sortingstation(1, constants.PIN_TRIGGER_1, constants.PIN_ECHO_1, constants.PIN_SERVO_1))
    sorting_stations.append(conveyoryeeter.sortingstation.Sortingstation(2, constants.PIN_TRIGGER_2, constants.PIN_ECHO_2, constants.PIN_SERVO_2))
    sorting_stations.append(conveyoryeeter.sortingstation.Sortingstation(3, constants.PIN_TRIGGER_3, constants.PIN_ECHO_3, constants.PIN_SERVO_3))
    
    while True:
        message= None

        ## message: (current_id, vehicle_id, loading_bay)
        if not queue.empty():
            message = queue.get(timeout=0.05)

            loading_bay= message[2]

            for i in range(0, loading_bay):
               
                sorting_station= sorting_stations[i]

                if i < loading_bay-1:
                    sorting_station.enqueue(False)
                elif i == loading_bay-1:
                    sorting_station.enqueue(True)
                else:
                    print("err")

            ## debug code      
            ##for i in range(nr_postazioni):
            ##    print(f"sorting station {i}: {sorting_stations[i].action_queue}")
                    

