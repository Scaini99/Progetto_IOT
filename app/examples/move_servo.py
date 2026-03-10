
from custom_lib.conveyoryeeter.diverterstation import DiverterStation
from custom_lib.conveyoryeeter.conveyorbeltengine import ConveyorBeltEngine
from time import sleep


def main():
    print("=== Test DiverterStation – push ogni 2 secondi ===")

    conveyorbelt= ConveyorBeltEngine(
        pin_rele= 21
    )

    conveyorbelt.start()

    station1 = DiverterStation(
        position=1,
        trig_pin=23,   # trigger sensore (non usato in questo test)
        echo_pin=24,   # echo sensore (non usato in questo test)
        servo_pin=13   # GPIO servo (BCM)
    )

    station2 = DiverterStation(
        position=2,
        trig_pin=25,   # trigger sensore (non usato in questo test)
        echo_pin=8,   # echo sensore (non usato in questo test)
        servo_pin=7   # GPIO servo (BCM)
    )

    try:
        while True:
            if station1.is_passing():
                print("Pacco rilevato stazione 1, spingo!")
                station1.push_package()
                
            if station2.is_passing():
                print("Pacco rilevato stazione 2, spingo!")
                station2.push_package()
                

    except KeyboardInterrupt:
        print("\nInterruzione manuale")
        conveyorbelt.stop()

    finally:
        print("Cleanup GPIO")
        station1.cleanup()
        station2.cleanup()
        conveyorbelt.cleanup()

if __name__ == "__main__":
    main()
