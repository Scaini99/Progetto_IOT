from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="sMister", timeout=10)

class Coordinate:
    '''
    Coordinate latitudine, longitudine
    '''
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

class Address:
    '''
    Indirizzi di casa
    '''
    def __init__(self, cap, provincia, comune, via, civico, interno=None):
        self.cap = cap
        self.provincia = provincia
        self.comune = comune
        self.via = via
        self.civico = civico
        self.interno = interno
        self.coordinate = self._get_coordinates()

    def _get_coordinates(self):
        query = f"{self.via} {self.civico}, {self.comune}, {self.provincia}, {self.cap}, Italia"
        location = geolocator.geocode(query)

        if location:
            return Coordinate(location.longitude, location.latitude)
        else:
            print(f"{query}: No results found for coordinates")
            return None