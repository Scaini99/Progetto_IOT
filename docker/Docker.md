
# Docker

Si è scelto di utilizzare Docker per rendere il progetto facilemte replicabile. Per installare Docker:

```sh
sudo apt install docker-compose
```

## Portainer

Per semplificare la gestione di Docker è stato installato Portainer, un’interfaccia grafica per amministrare i container.

```sh
docker-compose -f portainer.yaml up -d
```

```yaml
version: '3.8'

services:
  portainer:
    image: portainer/portainer-ce
    container_name: portainer
    restart: unless-stopped
    ports:
      - "9000:9000" #http
      - "9443:9443" #https
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /home/admin/sMister/docker/portainer:/data
```

## Stack

### metrics

Lo stack _metrics_ raccoglie i servizi basilari quali **Influxdb** e **Grafana**.

```yaml
version: '3.8'

  grafana:
    image: grafana/grafana
    container_name: grafana
    ports :
      - "3000:3000"
    user: "0"
    volumes:
      - /home/admin/sMister/docker/grafana:/var/lib/grafana
    restart: unless-stopped
    init: true
```

### Database

Questo stack contiene i servizi per gestire i database.

```yaml

version: "3.9"
services:
  postgres:
    image: postgres
    environment:
      POSTGRES_USER: "admin"
      POSTGRES_PASSWORD: "psqladmin"
    ports:
      - "5432:5432"
    volumes:
      - /home/admin/sMister/docker/postgres/data:/var/lib/postgresql/data
    container_name: postgresql
    restart: unless-stopped
    
  adminer:
    image: adminer
    restart: unless-stopped
    ports: 
      - 8080:8080
```

#### Postgres

Il databese che contiene le informazioni relative ai pacchi.

Al suo interno è presente un database `pacchi`.

```sql
CREATE TABLE dati_spedizione (
  numero_ordine INTEGER UNIQUE NOT NULL,
  cap INTEGER NOT NULL,
  provincia TEXT NOT NULL,
  comune TEXT NOT NULL,
  via TEXT NOT NULL,
  civico INTEGER NOT NULL,
  interno TEXT
);
```

```sql
CREATE TABLE consegna (
  numero_ordine INTEGER NOT NULL UNIQUE,
  veicolo_assegnato INTEGER NOT NULL,
  stato TEXT CHECK (stato IN ('in_magazzino', 'in_consegna', 'consegnato', 'tentata_consegna')) NOT NULL,
  ultimo_aggiornamento DATE NOT NULL,
  FOREIGN KEY (numero_ordine) REFERENCES dati_spedizione(numero_ordine)
);
```

#### Adminer

Programma che serve per gestire da un interfaccia grafica Postgres.


### routing

Lo stack _routing_ contiene i servizi necessari al routing dei pacchi, contiene VROOM e ORS.

Prima di tutto bisogna scaricare le mappe
```
mkdir -p ~/vroom-osrm/data
wget https://download.geofabrik.de/europe/italy/nord-est-latest.osm.pbf -O ~/vroom-osrm/data/map.osm.pbf

```

Dopodiché bisogna eseguire questo container per preparare le mappe

```
version: '3.8'

services:
  osrm-prep:
    image: osrm/osrm-backend
    command: >
      sh -c "
        osrm-extract -p /opt/car.lua /data/map.osm.pbf &&
        osrm-contract /data/map.osrm
      "
    volumes:
      - /home/thomas/vroom-osrm/data:/data
    restart: "no"

```

Una volta eseguito è meglio eliminarlo.

A questo punto è possibile installare i servizi di routing.

```yaml
version: '3.8'

services:
  osrm:
    network_mode: host ## todo
    image: osrm/osrm-backend
    command: osrm-routed /data/map.osrm
    volumes:
      - /home/thomas/vroom-osrm/data:/data
    ports:
      - "5000:5000"
    restart: unless-stopped

  vroom:
    network_mode: host ## todo
    image: ghcr.io/vroom-project/vroom-docker:v1.14.0
    environment:
      - VROOM_ROUTER=osrm
      - OSRM_HOST=osrm
      - OSRM_PORT=5000
    ports:
      - "3100:3000"
    depends_on:
      - osrm
    restart: unless-stopped
```

