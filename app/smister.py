## sMister
##
## Script per la gestione delle consegne
## venv: source venv/bin/activate

## Import librerie

import custom_lib.vroom_utils as vroom_utils        # interfaccia con vroom
import custom_lib.conveyoryeeter as conveyoryeeter  # nastro trasportatore 
from datetime import datetime                   
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="sMister", timeout=10) # ricerca indirizzi

import constants    # contiene le costanti
import psycopg2     # per database
import requests     # richieste in rete
import json         # maneggia file formato json

import threading    # uso dei thread
from queue import Queue, Empty  # code

## thread 
from qr_scan_thread import qr_reader
from phisical_stations_thread import phisical_stations
from conveyor_thread import conveyor_belt

def main():
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

    ## Inserimento pacchi di giornata in db
    ## api per inserire dati all'interno del db tamite csv
    ## PRE: connessione al db
    # - percorso al csv con i nuovi pacchi
    # - aggiunge pacchi al db
    ## POST: table "dati_spedizione" popolata

    ## Smistamento logico: vroom
    ## avviene schedulato ad una certa ora
    ## PRE: "dati_spedizione" popolata
    # - legge le consegne dalla table "dati_spedizione" 
    # - invoca il routing di vroom
    # - popola table "consegna"
    ## POST: table "consegna" popolata

    vroom_input= vroom_utils.input.Input()

    ##TODO: max pacchi per veicolo potrebbe essere i pacchi da consegnare oggi / NR_OF_VEHICLES
    max_pacchi= 5

    ## inizializzazione flotta con i veicoli disponibili
    for i in range(constants.NR_OF_VEHICLES):
        vehicle = vroom_utils.vehicle.Vehicle(i+1, max_pacchi, constants.BASE_COORD, constants.BASE_COORD)
        vroom_input.add_vehicle(vehicle)

    cur = database.cursor()

    print("ricerca pacchi da smistare...")
    cur.execute("SELECT numero_ordine, cap, provincia, comune, via, civico, interno FROM pacco")
    
    for row in cur.fetchall():
        job_id= row[0]

        job_cap= row[1]
        job_provincia= row[2]
        job_comune= row[3]
        job_via= row[4]
        job_civico= row[5]
        job_interno= row[6]

        address= f"{job_via}, {job_civico}, {job_cap}, {job_comune}, {job_provincia}, Italia"

        job_location= geolocator.geocode(address)

        job= vroom_utils.job.Job(id=job_id, location=[job_location.longitude, job_location.latitude])
        vroom_input.add_job(job)

    print("invio richiesta a Vroom")

    response = requests.post(
        'http://localhost:3000',
        json=vroom_input.to_dict(),
        headers={"Content-Type": "application/json"}
    )

    json_response = json.loads(response.text)

    print(response.text)

    ## tot pacchi da consegnare oggi
    tot_packages=0

    print("inserimento pacci in tavola consegne")
    for route in json_response['routes']:
        veicolo_assegnato = route['vehicle']
        for step in route['steps']:
            if step['type'] == 'job':
                numero_ordine = step['id']

                cur.execute(
                    "INSERT INTO consegna (numero_ordine, veicolo_assegnato) VALUES (%s, %s) ON CONFLICT (numero_ordine) DO NOTHING",
                    (numero_ordine, veicolo_assegnato)
                )
                tot_packages+=1

    database.commit()

    print("routing completato")

    ## Smistamento fisico
    ## avviene dopo lo smistamento logico
    ## PRE: table "cosegna" popolata
    # - attivazione nastro trasportatore
    # - attivazione fotocamera
    # - riconoscimento barcode
    # - smistamento in base a table "consegna"
    # - attivazione attuatori
    ## POST: table consegna aggiornata
    ##TODO:
    # tipo creare tutto

    ##nr_postazioni= constants.NR_OF_VEHICLES

    ##sorting_stations= []

    ## inizializzazione manuale delle stazioni di smistamento like a pro (posizione trigger echo servo)
    ##sorting_stations.append(conveyoryeeter.diverterstation.DiverterStation(1, constants.PIN_TRIGGER_1, constants.PIN_ECHO_1, constants.PIN_SERVO_1))
    ##sorting_stations.append(conveyoryeeter.diverterstation.DiverterStation(2, constants.PIN_TRIGGER_2, constants.PIN_ECHO_2, constants.PIN_SERVO_2))
    
    qr_read_queue = Queue()

    qr_reader_done = threading.Event()
    no_more_packages = threading.Event()

    ## Thread per il nastro trasportatotore
    conveyor_belt_thread = threading.Thread(target=conveyor_belt, args=(
        qr_reader_done, ## DONE: thread qr non ha piu pacchi da leggere
        no_more_packages ## DONE: le stazioni fisiche non hanno piu pacchi
    ))

    cur= database.cursor()
    cur.execute("SELECT COUNT(*) AS totale_pacchi FROM consegna;")
    result= cur.fetchone()
    to_be_smisted= result[0] ## int: nr di pacchi presenti

    qr_reader_thread = threading.Thread(target=qr_reader, args=(
        qr_read_queue, ## canale qr_scan_thread - phisical_stations_thread
        qr_reader_done, ## comunica la sua fine
        database, ## connessione al db
        to_be_smisted ## pacchi da smistare in giornata
    ))

    phisical_stations_thread = threading.Thread(target=phisical_stations, args=(
        qr_read_queue, ## canale qr_scan_thread - phisical_stations_thread
        no_more_packages, ## comunica la sua fine
        to_be_smisted ## pacchi da smistare in giornata
    ))

    conveyor_belt_thread.start()
    qr_reader_thread.start()
    phisical_stations_thread.start()

    print("end")
    

if __name__ == "__main__":
    main()