import custom_lib.conveyoryeeter as conveyoryeeter
import constants
import threading
import time



def conveyor_belt(stop_event: threading.Event):
    conveyorbelt_engine = conveyoryeeter.conveyorbeltengine.Conveyorbeltengine(constants.PIN_CTRL_CONVEYOR_BELT)
    print("conveyer start")
    
    conveyorbelt_engine.start()
    
    stop_event.wait() 
    
    
    conveyorbelt_engine.stop()
    print("conveyer stop")