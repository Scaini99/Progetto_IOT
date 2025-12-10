"""
Thread per la gestione del nastro trasportatore
- fa partire un nastro
- aspetta un segnale per spegnerlo
"""


import custom_lib.conveyoryeeter as conveyoryeeter
import constants
import threading
import time

def conveyor_belt(  qr_scan_thread_done: threading.Event,
                    phisical_station_thread_done: threading.Event
                ):

    conveyorbelt_engine = conveyoryeeter.conveyorbeltengine.ConveyorBeltEngine(constants.PIN_CTRL_CONVEYOR_BELT)
    print("conveyor_thread: START")
    
    conveyorbelt_engine.start()
    
    qr_scan_thread_done.wait()
    phisical_station_thread_done.wait()

    print("conveyor_thread: stopping in 10 seconds")
    time.sleep(10)

    print("conveyor_thread: STOP")
    conveyorbelt_engine.stop()
    

    