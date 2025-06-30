from custom_lib import geo_utils


indirizzo = geo_utils.Address("33100", "UD", "Udine", "Via delle scienze", "206", None)


print(indirizzo.coordinate.lat, indirizzo.coordinate.lon)