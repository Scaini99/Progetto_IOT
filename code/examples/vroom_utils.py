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
    def __init__(self, id, job_lat, job_long): ## TODO: inizializzare con indirizzo, non con latitudine logngitudine
        '''
        anziche longitudine e latitudine sarebbe carino avere un indirizzo... 
        '''
        self.id= id
        self.location= [job_lat, job_long]
        self.delivery= 1

    def add_delivery(self):
        '''
        Aggiunge un pacco da consegnare all'indirizzo
        '''
        self.delivery= self.delivery +1
    
    def to_dict(self):
        return {
            "id": self.id,
            "location": self.location,
            "delivery": self.delivery,
        }