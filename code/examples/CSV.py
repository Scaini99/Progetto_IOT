import csv
with open('code/routing_pacchi.csv', mode='r', newline='', encoding='latin1') as file:
    reader = csv.DictReader(file, delimiter=';')
    for riga in reader:
        
        print(riga['cap'], riga['città'], riga['indirizzo'])  
        import csv
import random

# Leggi il file esistente
with open('code/routing_pacchi.csv', mode='r', encoding='latin1') as infile:
    reader = csv.DictReader(infile, delimiter=';')
    righe = list(reader)

# Aggiungi un numero randomico a 6 cifre a ogni riga
for riga in righe:
    riga['codice'] = random.randint(100000, 999999)  # 6 cifre

# Scrivi un nuovo CSV con la colonna aggiunta
with open('code/routing_pacchi_codici.csv', mode='w', encoding='latin1', newline='') as outfile:
    intestazioni = righe[0].keys()  # tutte le colonne + 'codice'
    writer = csv.DictWriter(outfile, fieldnames=intestazioni, delimiter=';')
    writer.writeheader()
    writer.writerows(righe)
