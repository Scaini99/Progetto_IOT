
## Connettersi a db
## import librerie
## inizializzazione costanti
## inizializzazione flotta

## Inserimento pacchi di giornata in db
## api per inserire dati all'interno del db tamite csv
## PRE: connessione al db
# - percorso al csv con i nuovi pacchi
# - aggiunge pacchi al db
## POST: table "dati_spedizione" popolata
##TODO:
# wrapper per db con custom_lib

## Smistamento logico: vroom
## avviene schedulato ad una certa ora
## PRE: "dati_spedizione" popolata
# - legge le consegne dalla table "dati_spedizione" 
# - invoca il routing di vroom
# - popola table "consegna"
## POST: table "consegna" popolata
##TODO:
# refactoring minimo da smister.py

## Smistamento fisico
## avviene dopo lo smistamento logico
## PRE: table "cosegna" popolata
# - attivazione nastro trasportatore
# - attivazione fotocamera
# - riconoscimento barcode
# - smistamento in base a table "consegna"
# - attivazione attuatori
## POST: table consegna aggiornata
##TODO:
# tipo creare tutto

