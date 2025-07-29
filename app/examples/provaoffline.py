from geopy.geocoders import Nominatim
from pyrosm import OSM
from shapely.geometry import Point
import networkx as nx
import numpy as np
import time

# === PARAMETRI ===
PBF_PATH = "C:/Users/scain/Downloads/nord-est-latest.osm.pbf"
indirizzo_partenza = "Via Nasine 8, varmo"
indirizzo_arrivo = "via mantova 88, Udine"

# === STEP 1: Geocodifica (da indirizzo a coordinate) ===
geolocator = Nominatim(user_agent="distanza_osm_pbf")
def geocodifica(indirizzo):
    time.sleep(1)  # Per rispetto dei limiti Nominatim
    location = geolocator.geocode(indirizzo)
    if location:
        return (location.latitude, location.longitude)
    else:
        raise ValueError(f"❌ Indirizzo non trovato: {indirizzo}")

coord_start = geocodifica(indirizzo_partenza)
coord_end = geocodifica(indirizzo_arrivo)
print(f"Coordinate partenza: {coord_start}")
print(f"Coordinate arrivo: {coord_end}")

# === STEP 2: Costruisci grafo da .osm.pbf ===
print("costruisco il grafo")
osm = OSM(PBF_PATH)
print("caricato file")
#si generano probemi co n la funzione edges, sarebbe da vedere qual'è il problema
edges = osm.get_network(network_type="walking")  # o "driving", "cycling"
print("fatto")
#G = get_networkx_graph(edges, graph_type="networkx", directed=True)

# === STEP 3: Nodo più vicino ===
print("ricerco il nodo")
def get_nearest_node(G, point):
    nodes = list(G.nodes(data=True))
    coords = np.array([[data['x'], data['y']] for _, data in nodes])
    dists = np.linalg.norm(coords - np.array([point.x, point.y]), axis=1)
    idx = np.argmin(dists)
    return nodes[idx][0]

start_point = Point(coord_start[1], coord_start[0])  # lon, lat
end_point = Point(coord_end[1], coord_end[0])

start_node = get_nearest_node(G, start_point)
end_node = get_nearest_node(G, end_point)

# === STEP 4: Calcolo percorso ===
print("calcolo il percorso")
try:
    path = nx.shortest_path(G, start_node, end_node, weight="length")
    distance = nx.shortest_path_length(G, start_node, end_node, weight="length")
    print(f"Distanza: {distance:.2f} metri")
except nx.NetworkXNoPath:
    print("⚠️ Nessun percorso trovato tra i due indirizzi nel grafo.")
