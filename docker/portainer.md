installato su raspberry tramite cmp docker e portainer per una interfaccia grafica per docker
```yaml
version: '3.8'

services:
  portainer:
    image: portainer/portainer-ce
    container_name: portainer
    restart: unless-stopped
    ports:
      - "9000:9000"
      - "8000:8000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ~/progetto/portainer:/data

volumes:
  portainer_data:
```
installato tramite portainer influxdb
```yaml
version: '3.8'

services:
  influxdb2:
    image: uniud4iot/influxdb2:v2.2.1-armv7l
    container_name: influxdb2
    ports:
      - "8086:8086"
    volumes:
      - ~/admin/progetto/influxdb:/root/.influxdbv2
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
    command: influxd
    restart: unless-stopped
```
dentro influx è stato crato il bucket pacchi
```bash
docker exec influxdb2 influx bucket create -n pacchi  -o progetto  -t <token>
```
creati due utenti in influxdb chiamati phyton e grafana
```bash
ocker exec influxdb2 influx user create -n <utente> -p <password> -o progetto -t <token>
```
