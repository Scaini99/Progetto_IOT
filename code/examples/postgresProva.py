import psycopg2
import pandas


#---------------------------collegamento al database con visualizzazione della tabella--------------------
database = psycopg2.connect( host="192.168.1.82",
                           port=5432,
                           database="pacchi",
                           user="admin",
                           password="psqladmin")

#----------------------------------funziona---------------------------------------------------------------

#-------------------------------caricamento dati csv sulla tabella----------------------------------------
selettore = database.cursor()

with open(r"C:\Users\scain\OneDrive\Desktop\provaCaricamento.csv", "r", encoding="utf-8") as f: # Salta intestazione CSV (header)
        next(f)
        selettore.copy_expert("COPY dati_spedizione FROM STDIN WITH CSV", f)

database.commit()


print("Dati caricati con successo!")
db=pandas.read_sql("SELECT*FROM dati_spedizione", database)
print(db)
selettore.close()
database.close()