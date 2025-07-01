from custom_lib.geo_utils import Address

## coordinate di un punto di smistamento
indirizzo = Address("33033", "UD", "Codroipo", "Via circonvallazione sud", "80", None)


print(indirizzo.coordinate.lat, indirizzo.coordinate.lon)