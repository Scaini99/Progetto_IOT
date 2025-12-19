
from custom_lib.conveyoryeeter.diverterstation import DiverterStation
from time import sleep


def main():
    print("=== Test DiverterStation – push ogni 2 secondi ===")


    station = DiverterStation(
        position=1,
        trig_pin=23,   # trigger sensore (non usato in questo test)
        echo_pin=24,   # echo sensore (non usato in questo test)
        servo_pin=13   # GPIO servo (BCM)
    )

    try:
        while True:
            print("Spingo pacco...")
            station.push_package()
            sleep(2)

    except KeyboardInterrupt:
        print("\nInterruzione manuale")

    finally:
        print("Cleanup GPIO")
        station.cleanup()


if __name__ == "__main__":
    main()
