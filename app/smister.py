## sMister
##
## Script per la gestione delle consegne
##

## Import librerie

import custom_lib.vroom_utils as vroom_utils
from datetime import datetime
from geopy.geocoders import Nominatim

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

## Inserimento pacchi di giornata in db
## api per inserire dati all'interno del db tamite csv
## PRE: connessione al db
# - percorso al csv con i nuovi pacchi
# - aggiunge pacchi al db
## POST: table "dati_spedizione" popolata
##TODO:
# wrapper per db con custom_lib (serve?)

## Smistamento logico: vroom
## avviene schedulato ad una certa ora
## PRE: "dati_spedizione" popolata
# - legge le consegne dalla table "dati_spedizione" 
# - invoca il routing di vroom
# - popola table "consegna"
## POST: table "consegna" popolata

vroom_input= vroom_utils.input.Input()

##TODO: max pacchi per veicolo potrebbe essere i pacchi da consegnare oggi / NR_OF_VEHICLES
max_pachi= 3

## inizializzazione flotta con i veicoli disponibili
for i in range(constants.NR_OF_VEHICLES):
    vehicle = vroom_utils.vehicle.Vehicle(i+1, max_pacchi, constants.BASE_COORD, constants.BASE_COORD)
    vroom_input.add_vehicle(vehicle)

cur = database.cursor()
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

response = requests.post(
    'http://localhost:3000',
    json=vroom_input.to_dict(),
    headers={"Content-Type": "application/json"}
)

json_response = json.loads(response.text)

print(response.text)


for route in json_response['routes']:
    veicolo_assegnato = route['vehicle']
    for step in route['steps']:
        if step['type'] == 'job':
            numero_ordine = step['id']

            cur.execute(
                "INSERT INTO consegna (numero_ordine, veicolo_assegnato) VALUES (%s, %s)",
                (numero_ordine, veicolo_assegnato)
            )

database.commit()




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
"""
pseudo:
    /*inizializzate in constants*/
    LIST_ECHO_PINS
    LIST_TRIGGER_PINS
    LIST_SERVO_PINS

    conveyorsistem(conveypyengine)

    nr_postazioni= NR_OF_VEHICLES
    
    // aggiunge sortingstations al sistema di smistamento
    for i in 1..nr_postazioni{
        sortingstation= New Sortingstation(i, LIST_TRIGGER_PIN[i], LIST_ECHO_PIN[i], LIST_SERVO_PINS[i])
        conveyorsistem.add_sortingstation(sortingstation)
    }

    // costruito il sistema di smistamento

    while pacchi_da_smistare > 0{

        id= scannerizza_fotocamera()

        // già, non sto parallelizzado, sono proprio un marpione
        // cmq
        // se la fotocamera legge un valore, aggiorna le relative postazioni di smistamento
        if id!= null{
            for i in 1..id{
                // funziona se passato by reference
                sortingstation= conveyorsistem.get_sortingstation(i)

                if i < id {
                    sortingstation.enqueue(False)
                }if i == id {
                    sortingstation.enqueue(True)
                }else {
                    //errore... 
                }

            }
        }

        // le postazioni controllano se gli passa un pacco davanti
        for i in 1..nr_postazioni{
            postazione= coveyorsystem.get_sortingstation(i)

            if postazione.is_passing(){
                azione= postazione.dequeue()

                if azione == True{
                    postazione.push_package()
                }
            }
        }
        
    }
"""

