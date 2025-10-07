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
import time


def phisical_stations(queue: Queue, stop_event: threading.Event):
    nr_postazioni= 3 # constants.NR_OF_VEHICLES


    ## inizializzazione postazioni (position, trigger, echo, servo)
    
    sorting_stations= []
    sorting_stations.append(conveyoryeeter.sortingstation.DiverterStation(1, constants.PIN_TRIGGER_1, constants.PIN_ECHO_1, constants.PIN_SERVO_1))
    sorting_stations.append(conveyoryeeter.sortingstation.DiverterStation(2, constants.PIN_TRIGGER_2, constants.PIN_ECHO_2, constants.PIN_SERVO_2))
    sorting_stations.append(conveyoryeeter.sortingstation.DiverterStation(3, constants.PIN_TRIGGER_3, constants.PIN_ECHO_3, constants.PIN_SERVO_3))
    
    while not stop_event.is_set():
        message= None

        ## message: (current_id, vehicle_id, loading_bay)
        if not queue.empty():
            print("phisical_station_thread: FOUND MSG")
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

        for i in range(nr_postazioni):
            sorting_station= sorting_stations[i]
            if sorting_station.is_passing():
                instruction= sorting_station.dequeue()
                print(f"phisical_station_thread: SMTH FOUND, INSTRUCTION: {instruction}")
                if instruction:
                    sorting_station.push_package()
        
        time.sleep(0.01)

