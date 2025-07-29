import psycopg2
import pandas
import datetime


#---------------------------collegamento al database con visualizzazione della tabella--------------------
database = psycopg2.connect( 
                           host="localhost",
                           port=5432,
                           database="centro_smistamento",
                           user="admin",
                           password="psqladmin"
                           )

#----------------------------------funziona---------------------------------------------------------------
print(datetime.date.today())
#-------------------------------caricamento dati csv sulla tabella----------------------------------------
selettore = database.cursor()

with open(r"", "r", encoding="utf-8") as f: # Salta intestazione CSV (header)
        next(f)
        selettore.copy_expert("COPY pacco FROM STDIN WITH CSV", f)

database.commit()


print("Dati caricati con successo!")
db=pandas.read_sql("SELECT*FROM dati_spedizione", database)
print(db)
selettore.close()
database.close()