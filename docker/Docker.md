
# Docker

## Portainer

Per semplificare la gestione di Docker è stato installato Portainer, un’interfaccia grafica per amministrare i container.

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

services:
  influxdb2:
    image: uniud4iot/influxdb2:v2.2.1-armv7l
    container_name: influxdb2
    ports:
      - "8086:8086"
    volumes:
      - /home/admin/sMister/docker/influxdb:/root/.influxdbv2
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
    command: influxd
    restart: unless-stopped

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

#### Influxdb

Influxdb è il database del sistema.

Una prima configurazione prevede la creazione del database contenente i pacchi e le loro informazioni:

```bash
docker exec influxdb2 influx bucket create -n pacchi  -o sMister-t <token>
```

Per una gestione più ordinata sono stati creati due utenti distinti: _python_ e _grafana_.

```bash
docker exec influxdb2 influx user create -n python -p <password> -o sMister -t <token>
docker exec influxdb2 influx user create -n grafana -p <password> -o sMister -t <token>
```
L'utente _python_ dispone dei permessi di lettura e scrittura, mentre l'utente _grafana_ solo di lettura.

```bash
docker exec influxdb2 influx auth create -u python -d readwrite_db --write-bucket <IDbucket> --read-bucket <IDbucket> -o sMister -t <token>
docker exec influxdb2 influx auth create -u grafana -d read_db --read-bucket <IDbucket> -o sMister -t <token>
```
### routing

Lo stack _routing_ contiene i servizi necessari al routing dei pacchi, contiene VROOM e ORS.

