## sMister
##
## Script per la gestione delle consegne
##

## Import librerie
import psycopg2
import json

import requests

from custom_lib.vroom_utils import Vehicle, Job, VROOM_LINK

## const
POSTGRESUSER= "admin"
POSTGRESPASSWORD= "psqladmin"

## Connessione al db
database = psycopg2.connect( 
                            host="localhost",
                            port=5432,
                            database="pacchi",
                            user= POSTGRESUSER,
                            password= POSTGRESPASSWORD
                           )

try:
    database
    print("Connessione attiva")
except NameError:
    print("Connessione non avvenuta")


## generazione lista dei veicoli
fleet= []

for i in range(0,10): ## 10 veicoli 
    vehicle= Vehicle(i, 10)
    fleet.append(vehicle.to_dict())

## query al database per cercare le consegne da fare oggi
cur = database.cursor()
cur.execute("SELECT numero_ordine, cap, provincia, comune, via, civico, interno FROM dati_spedizione")  # Esegue la query SQL

jobs = []  
for row in cur.fetchall():
    job = Job(*row)
    jobs.append(job)


#print(jobs[0].location)


request = {
    "vehicles": fleet,
    "jobs": [job.to_dict() for job in jobs]
}

#print(request)

response = requests.post(
    'http://localhost:3000',
    json=request,
    headers={"Content-Type": "application/json"}
)

##print(json.dumps(response, indent=2))

print(response)