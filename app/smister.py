## sMister
##
## Script per la gestione delle consegne
##

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
max_pacchi= 3

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

## strumentopolo ch eci servira piu avanti
tot_packages=0

for route in json_response['routes']:
    veicolo_assegnato = route['vehicle']
    for step in route['steps']:
        if step['type'] == 'job':
            numero_ordine = step['id']

            cur.execute(
                "INSERT INTO consegna (numero_ordine, veicolo_assegnato) VALUES (%s, %s)",
                (numero_ordine, veicolo_assegnato)
            )
            tot_packages+=1

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

nr_postazioni= constants.NR_OF_VEHICLES

sorting_stations= []

## inizializzazione manuale delle stazioni di smistamento like a pro
sorting_stations.append(conveyoryeeter.sortingstation.Sortingstation(1, 10, 11, 21))
sorting_stations.append(conveyoryeeter.sortingstation.Sortingstation(2, 12, 13, 22))
sorting_stations.append(conveyoryeeter.sortingstation.Sortingstation(3, 14, 15, 23))


## YOOO, entriamo nel ciclo di smistamento vero e proprio, finalmente, 
## da qua è tutto uno perche non parallelizziamo come dei pros
## ma comunque il nastro dovrebbe essere abbastanza lento
## mica siamo amazoz qua

## TODO: AGGIUNGI ATTIVAZIONE NASTRO
while tot_packages > 0:

    ## prima di tutto legge da fotocamera
    id = 1001   # TODO, IMPLEMENTARE ROBA FOTOCAMERA, MAGARI IN MANIERA NON BLOCCANTE, SE FOSSE POSSIBELE, PER CORTESIA, MI SAREBBE VERAMENTE UTILE SAI COM'E', POI SENNO SI BLOCCA TUTTO ED E' UN PO' UN PROBLEMA, QUINDI SE RIESCI FAI IN MODO CHE QUESTA CHIAMATA NON BLOCCHI IL RESTO DELL'ESECUZIONE DEL PROGRAMMA
                # grazie :)

    loading_bay= 1 # selectfrom"table" la loadingbay dedicata, potevamo farlo senza scomodare il db? si. sarebbe stato piu' efficente? si. ho voglia di implementarlo ora? no, il db fa figo

    if id!= None:
        print(id)
        for i in range(loading_bay):
            sorting_station= sorting_stations[i]

            if i < loading_bay:
                sorting_station.enqueue(False)
            if i == loading_bay :
                sorting_station.enqueue(True)
            else:
               print("err") 

    ## ora controlliamo le postazioni varie per vedere se c'e' un pacco davanti
    for i in range(nr_postazioni):
        sorting_station= sorting_stations[i]

        if sorting_station.is_passing():
            azione= sorting_station.dequeue()
            if azione == True:
                sorting_station.push_package()
    tot_packages=0## eliminami poi

"""
pseudo:

    QUESTO PSEUDO E' DA CONTROLLARE PER SPUNTI FUTURI, ORA E' UN PO OUTDATED
    /*inizializzate in constants*/
    LIST_ECHO_PINS
    LIST_TRIGGER_PINS
    LIST_SERVO_PINS

    conveyorsistem(conveypinengine)

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

