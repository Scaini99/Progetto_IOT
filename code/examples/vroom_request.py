## interfaccia per simulare
## curl -X POST -H "Content-Type: application/json" \
##    -d @request.json \
##    http://solver.vroom-project.org/ >> response.json

import json
import requests
import psycopg2

from custom_lib.vroom_utils import Vehicle, Job, VROOM_LINK

## request a db i veicoli disponibili
vehicles= []

for i in range(0,10):
    vehicle= Vehicle(i, 10)
    vehicles.append(vehicle.to_dict())

## request a influx di ordini da evadere
database = psycopg2.connect( host="192.168.1.82",
                           port=5432,
                           database="pacchi",
                           user="admin",
                           password="psqladmin")

cur = database.cursor()
cur.execute("SELECT numero_ordine, cap, provincia, comune, via, civico, interno FROM dati_spedizione")

jobs = []
for row in cur.fetchall():
    job = Job(*row)
    jobs.append(job)

print(jobs[0].location)



request = {
    "vehicles": vehicles,
    "jobs": [job.to_dict() for job in jobs]
}

print(request)


response = requests.post(
    VROOM_LINK,
    json=request,
    headers={"Content-Type": "application/json"}
)

##with open("response.json", "w") as f:
##    f.write(response.text)