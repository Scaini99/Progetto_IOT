
# Docker


Si è scelto di utilizzare Docker per rendere il progetto facilemte replicabile. Per installare Docker:

```sh
sudo apt install docker-compose
```

## Portainer

Per semplificare la gestione di Docker è stato installato Portainer, un’interfaccia grafica per amministrare i container.

Dentro la cartella  `smister/dockerservices/portainer` creare il file `portainer.yaml`:

```yaml
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
      - /home/pi/smister/dockerservices/portainer:/data
```

Per creare il container bisogna eseguire:

```sh
docker-compose -f portainer.yaml up -d
```
## Stack

### Database

Questo stack contiene i servizi per gestire i database.

```yaml
services:
  postgres:
    image: postgres
    environment:
      POSTGRES_USER: "admin"
      POSTGRES_PASSWORD: "psqladmin"
    ports:
      - "5432:5432"
    volumes:
      - /home/pi/smister/dockerservices/database/postgres/data:/var/lib/postgresql/data
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

Il primo accesso viene eseguito tramite **Adminer**.

Apri browser su http://<ip_del_server>:8080 
  - System: PostgreSQL
  - Server: postgres 
  - Username: admin
  - Password: psqladmin

Al suo interno deve esserecreato un database `centro_smistamento`.

La tabella pacchi contiene tutto i pacchi che sono transitati per il centro di smistamento.

```sql
CREATE TABLE pacco (
  numero_ordine INTEGER UNIQUE NOT NULL,
  cap INTEGER NOT NULL,
  provincia TEXT NOT NULL,
  comune TEXT NOT NULL,
  via TEXT NOT NULL,
  civico INTEGER NOT NULL,
  interno TEXT,
  stato TEXT CHECK (stato IN ('in_magazzino', 'in_consegna', 'consegnato', 'tentata_consegna')) NOT NULL,
  ultimo_aggiornamento TIMESTAMP(0) NOT NULL,
);
```

La tabella consegna permette di tracciare ogni pacco all'interno del sistema.

```sql
CREATE TABLE consegna (
  numero_ordine INTEGER NOT NULL UNIQUE,
  veicolo_assegnato INTEGER NOT NULL,
  FOREIGN KEY (numero_ordine) REFERENCES pacco(numero_ordine)
);
```

#### Adminer

Programma che serve per gestire da un interfaccia grafica Postgres.

Vedi Postgres.


### Routing

Lo stack _routing_ contiene i servizi necessari al routing dei pacchi, contiene VROOM e ORS.

Prima di tutto bisogna scaricare le mappe

```bash
mkdir  /home/pi/smister/dockerservices/routing/map
wget https://download.geofabrik.de/europe/italy/nord-est-latest.osm.pbf -O /home/pi/dockerservices/routing/map/map.osm.pbf
```

Dopodiché bisogna eseguire questo container per preparare le mappe. Questa è un operazione che può essere fatta anche a mano se non si vuole creare il container

```yaml
services:
  osrm-prep:
    image: osrm/osrm-backend
    command: >
      sh -c "
        osrm-extract -p /opt/car.lua /data/map.osm.pbf &&
        osrm-contract /data/map.osrm
      "
    volumes:
      - /home/pi/smister/dockerservices/routing/map:/data
    restart: "no"
```

Bisogna aspettare qualche minuto che estragga le mappe, controlla sul log illivello di avanzamento. Una volta terminato di eseguire questo container non è più indispensabile.

A questo punto è possibile installare i servizi di routing.

```yaml
services:
  osrm:
    network_mode: host ## todo
    image: osrm/osrm-backend
    command: osrm-routed /data/map.osrm
    volumes:
      - /home/pi/smister/dockerservices/routing/osrm:/config
      - /home/pi/smister/dockerservices/routing/map:/data
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
    volumes:
      - /home/pi/smister/dockerservices/routing/vroom:/config
    ports:
      - "3100:3000"
    depends_on:
      - osrm
    restart: unless-stopped
```

