
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

#### Adminer

Programma che serve per gestire da un interfaccia grafica Postgres.


### routing

Lo stack _routing_ contiene i servizi necessari al routing dei pacchi, contiene VROOM e ORS.

```yaml
version: '3.8'

services:
  vroom:
    image: ghcr.io/vroom-project/vroom-docker:v1.14.0
    container_name: vroom
    environment:
      - VROOM_ROUTER=osrm  # Routing layer (osrm, valhalla, ors)
    ports:
      - "3100:3000"
    volumes:
      - /home/admin/sMister/docker/VROOM/conf:/conf  # Mapped volume for config & log files
    restart: unless-stopped
```

