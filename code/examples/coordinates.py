from geo_utils import Address

indirizzo = Address("33100", "UD", "Udine", "Via delle scienze", "206", None)


print(indirizzo.coordinate.lat, indirizzo.coordinate.lon)