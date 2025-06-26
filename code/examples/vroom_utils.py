from geo_utils import Address

VROOM_LINK = 'http://solver.vroom-project.org/' ## da cambiare con host

## Coordinate della base per le consegne
base_lat = 45.0
base_lon= 11.0

class Vehicle:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.start= [base_lat, base_lon]

    def to_dict(self):
        return {
            "id": self.id,
            "capacity": self.capacity,
            "start": self.start,
        }

class Job:
    '''
    Classe che rappresenta una consegna ad una casa
    '''
    def __init__(self, numero_ordine, cap, provincia, comune, via, civico, interno):
        self.numero_ordine= numero_ordine
        self.indirizzo = Address(cap, provincia, comune, via, civico, interno)
        self.location= [self.indirizzo.coordinate.lat, self.indirizzo.coordinate.lon]
        self.delivery= 1

    def add_delivery(self):
        '''
        Aggiunge un pacco da consegnare all'indirizzo
        '''
        self.delivery= self.delivery +1
    
    def to_dict(self):
        return {
            "id": self.numero_ordine,
            "location": self.location,
            "delivery": self.delivery,
        }