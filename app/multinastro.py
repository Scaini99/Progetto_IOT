import threading
from time import sleep

# Simulazione
from custom_lib.conveyoryeeter.sortingstation import Sortingstation
from custom_lib.conveyoryeeter.watchmypack import WatchMyPack
import constants






## sMister
##
## Script per la gestione delle consegne
##

## Import librerie

import custom_lib.vroom_utils as vroom_utils        # interfaccia con vroom
import custom_lib.conveyoryeeter as conveyoryeeter  # nastro trasportatore 
from datetime import datetime                   
from geopy.geocoders import Nominatim

from custom_lib.conveyoryeeter.watchmypack import WatchMyPack
import cv2

from time import sleep

geolocator = Nominatim(user_agent="sMister", timeout=10) # ricerca indirizzi

import constants    # contiene le costanti
import psycopg2     # per database
import requests     # richieste in rete
import json         # maneggia file formato json

## Connettersi a db

database = psycopg2.connect( 
                            host=constants.DBHOST,
                            port=constants.DBPORT,
                            database=constants.DBNAME,
                            user= constants.DBUSER,
                            password= constants.DBPASSWORD
                           )
try:
    database
    print("Connessione database attiva")
except NameError:
    print("Connessione database non avvenuta")

## from here:

tot_packages = 10
current_id = None

nr_postazioni= constants.NR_OF_VEHICLES




# Inizializza fotocamera e stazioni
camera = WatchMyPack(camera_id=0)
sorting_stations = []

sorting_stations= []

## inizializzazione manuale delle stazioni di smistamento like a pro
sorting_stations.append(Sortingstation(1, 10, 11, 21))
sorting_stations.append(Sortingstation(2, 12, 13, 22))
sorting_stations.append(Sortingstation(3, 14, 15, 23))

# === Thread camera che comunica direttamente con sorting_stations ===
def camera_thread():
    prev_id= -1

    pacchi_da_smistare = 10
    while pacchi_da_smistare > 0:
        qr_data = camera.read_qr_code()

        if qr_data and qr_data != prev_id:
            prev_id= qr_data
            current_id = qr_data
            print("QR Code rilevato:", current_id)

            cur = database.cursor()
            cur.execute("SELECT veicolo_assegnato FROM consegna WHERE numero_ordine = %s", (current_id,))
        
            result = cur.fetchone()
            vehicle_id = result[0]
            loading_bay= result[0] -1

            if vehicle_id != None:
                print("adding package to loading bay: " + str(loading_bay))
                for i in range(loading_bay+1):
                    sorting_station= sorting_stations[i]

                    if i < loading_bay:
                        sorting_station.enqueue(False)
                        print("aggiunto False a " + str(i))
                    elif i == loading_bay :
                        sorting_station.enqueue(True)
                        print("aggiunto True a " + str(i))
                    else:
                        print("err, out of vehicles")
                    

            pacchi_da_smistare -= 1
            sleep(1)

        sleep(0.1)  # evita loop troppo veloce

# === Thread sorting stations che fanno il push ===
def sorting_thread():
    while True:

        queue_length= sorting_stations[0].queue_length()
        print(queue_length)
        sleep(1)

# Avvio dei thread
camera_t = threading.Thread(target=camera_thread)
sorting_t = threading.Thread(target=sorting_thread)

camera_t.start()
sorting_t.start()

camera_t.join()

print("[MAIN] Fine pacchi da smistare. Puoi terminare il programma.")

