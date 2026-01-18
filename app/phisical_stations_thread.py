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

def phisical_stations(queue: Queue, done_event: threading.Event, to_be_smisted: int):
    print("phisical_station_thread: START")
    nr_postazioni= constants.NR_OF_VEHICLES
    internal_package_counter= 0

    ## inizializzazione postazioni (position, trigger, echo, servo)
    
    diverter_stations= []
    diverter_stations.append(conveyoryeeter.diverterstation.DiverterStation(1, constants.PIN_TRIGGER_1, constants.PIN_ECHO_1, constants.PIN_SERVO_1))
    diverter_stations.append(conveyoryeeter.diverterstation.DiverterStation(2, constants.PIN_TRIGGER_2, constants.PIN_ECHO_2, constants.PIN_SERVO_2))
    
    while internal_package_counter < to_be_smisted:
        message= None

        ## message: (current_id, vehicle_id, loading_bay)
        if not queue.empty():
            print("phisical_station_thread: FOUND MSG")
            message = queue.get(timeout=0.05)
            internal_package_counter= internal_package_counter +1

            loading_bay= message[2] ## loading_bay

            ## inserisce le istruzioni nelle code
            for i in range(0, loading_bay):
               
                diverter_station= diverter_stations[i]

                if i < loading_bay-1:
                    diverter_station.enqueue(False)
                elif i == loading_bay-1:
                    diverter_station.enqueue(True)
                else:
                    print("err")

            ## debug code      
            ##for i in range(nr_postazioni):
            ##    print(f"sorting station {i}: {diverter_stations[i].action_queue}")

        ## controlla le varie postazioni
        for i in range(nr_postazioni):
            diverter_station= diverter_stations[i]
            if diverter_station.is_passing():
                instruction= diverter_station.dequeue()
                print(f"phisical_station_thread: SMTH FOUND, INSTRUCTION: {instruction}")
                if instruction:
                    diverter_station.push_package()
        
        time.sleep(0.01)

    done_event.set()
