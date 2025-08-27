


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

camera = WatchMyPack(camera_id=0)
tot_packages = 10
current_id = None

nr_postazioni= constants.NR_OF_VEHICLES

sorting_stations= []

## inizializzazione manuale delle stazioni di smistamento like a pro
sorting_stations.append(conveyoryeeter.sortingstation.Sortingstation(1, 10, 11, 21))
sorting_stations.append(conveyoryeeter.sortingstation.Sortingstation(2, 12, 13, 22))
sorting_stations.append(conveyoryeeter.sortingstation.Sortingstation(3, 14, 15, 23))


while tot_packages > 0:
    qr_data = camera.read_qr_code()

    if qr_data:
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
                    
        tot_packages= 0



camera.stop()
cv2.destroyAllWindows()
