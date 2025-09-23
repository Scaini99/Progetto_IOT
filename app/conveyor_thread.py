"""
Thread per la gestione del nastro trasportatore
- fa partire un nastro
- aspetta un segnale per spegnerlo
"""


import custom_lib.conveyoryeeter as conveyoryeeter
import constants
import threading
import time

def conveyor_belt(stop_event: threading.Event):
    conveyorbelt_engine = conveyoryeeter.conveyorbeltengine.Conveyorbeltengine(constants.PIN_CTRL_CONVEYOR_BELT)
    print("conveyor_thread: START")
    
    conveyorbelt_engine.start()
    

    stop_event.wait() 

    print("conveyor_thread: STOP")
    conveyorbelt_engine.stop()
    

    