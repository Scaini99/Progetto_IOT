## Thread che spinge
## gestisce le push stations
## dalla queue deve estrarre un elemento (current_id, vehicle_id, loading_bay)
## e tramite loading_bay gestire la logica
## inoltre
## se sente passare un pacco davanti ad una station deve decidere se deviarlo o meno
from queue import Queue
import threading
import custom_lib.conveyoryeeter as conveyoryeeter  # nastro trasportatore
import constants


def phisical_stations(queue: Queue, stop_event: threading.Event):
    nr_postazioni= constants.NR_OF_VEHICLES


    ## inizializzazione postazioni
    ## TODO: PIN
    sorting_stations= []
    sorting_stations.append(conveyoryeeter.sortingstation.Sortingstation(1, 10, 11, 21))
    sorting_stations.append(conveyoryeeter.sortingstation.Sortingstation(2, 12, 13, 22))
    sorting_stations.append(conveyoryeeter.sortingstation.Sortingstation(3, 14, 15, 23))
    
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
                    

