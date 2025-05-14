## interfaccia per simulare
## curl -X POST -H "Content-Type: application/json" \
##    -d @request.json \
##    http://solver.vroom-project.org/ >> response.json

import json
import requests

from vroom_utils import Vehicle, Job, VROOM_LINK



vehicles= []

for i in range(0,10):
    vehicle= Vehicle(i, 10)
    vehicles.append(vehicle.to_dict())

jobs= []## TODO: trovare i jobs dagli indirizzi su influx

request = {
    "vehicles": vehicles,
    "jobs": jobs
}

print(request)

job= Job

response = requests.post(
    VROOM_LINK,
    json=request,
    headers={"Content-Type": "application/json"}
)

##with open("response.json", "w") as f:
##    f.write(response.text)