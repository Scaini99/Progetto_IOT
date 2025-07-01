from custom_lib.geo_utils import Address


indirizzo = Address("33030", "UD", "Varmo", "Via Giovanni Antonio", "7", None)


print(indirizzo.coordinate.lat, indirizzo.coordinate.lon)