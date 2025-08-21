# sMister

## Struttura progetto

NB: gitignore su dockerservices: questa cartella serve solo come root per i servizi docker, è da aggiornare anche nei docker.

## Idea 

L'idea di sMister nasce dalla crescente necessità da parte delle aziende di sistemi automatizzati che rendano più veloce ed efficiente lo smistamento dei pacchi. Questo sistema permette ad un centro logistico di ottimizzare il processo di consegna calcolando i percorsi ottimali per i corrieri e gestendo il flusso dei pacchi dal magazzino fino al veicolo di consegna.

Obiettivi del progetto

- Ottimizzare i percorsi dei corrieri per migliorare l'efficienza delle consegne
- Ridurre al minimo l'intervento umano nella gestione dei pacchi
- Realizzare un sistema facilmente replicabile e scalabile
- Limitare la dipendenza da servizi di terze parti

## Tecnologie

### Hardware

Per quanto riguarda la piattaforma hardware, si è scelto di utilizzare un Raspberry Pi 5 ovvero un single board computer sufficientemente prestante da supportare un sistema operativo e dotato di pin GPIO utili per il collegamento di componenti esterni. 

TODO: schema hardware

### Software

Il core del progetto è stato sviluppato in Python. Questo linguaggio è stato scelto per via della sua facilità di prototipazione e dell'ampia disponibilità di librerie.

TODO: metodo software

### Servizi

Parte fondamentale del progetto sono i servizi Docker che permettono al sistema di essere facilmente configurabile e integrabile in vari ambienti grazie a vari servizi Docker installati in locale. Sono stati usati i seguenti servizi:

- Portainer: interfaccia grafica web che permette l'installazione di container in maniera semplificata
- Postgres: il database che contiene le informazioni relative ai pacchi
- Adminer: programma che serve per gestire da un interfaccia grafica Postgres
- VROOM: servizio che fornisce un sistema di routing ottimale
- OSRM: motore open source per il calcolo di percorsi stradali

I servizi sono stati organizzati in stack dedicati, in modo da raggruppare componenti funzionalmente simili.

## Funzionamento

sMister interroga il database per ottenere l'elenco delle consegne previste e riceve come risposta gli indirizzi dei colli associati. Queste informazioni sono trasformate in jobs, ovvero lavori di consegna da effettuare e, in base alla flotta di veicoli per le consegne disponibili, delega a VROOM il calcolo dei percorsi ottimali per ogni veicolo. 

Una volta calcolato ciò, il sistema deve riconoscere l'id del pacco su un nastro trasportatore per indirizzarlo verso la baia di carico corretta: questo viene fatto tramite un codice a barre che identifica unicamente ogni pacco. Lungo la linea alcuni attuatori si occupano di consegnare alla zona di carico giusta ogni pacco.

## Fasi 

Il sistema funziona in varie fasi separate e sequenziali.

### Requisiti

I requisiti perchè il sistema possa funzionare sono quelli di avere una connessione ad un database con le informazioni riguardanti i pacchi presenti in magazzino. È necessario che ogni pacco abbia un codice univoco, un indirizzo di spedizione e uno stato che indica se il pacco sia ancora da consegnare o meno (ritiri in sede, consegne mancate, ...). 

### Fase 1

Una volta avvenuta la connessione al database, _sMister_ interroga il database sui pacchi che abbiano il flag specifico per la consegna. Utilizzando i dati ricevuti ricava le coordinate geografiche delle consegne e, in base ai veicoli disponibili, compone un messaggio per il servizio di routing _VROOM_.

### Fase 2

Il messaggio generato durante la fase precedente viene inviato al servizio di routing in locale. Quest'ultimo ritorna una risposta che viene elaborata per inserire nel database le informazioni riguardanti la consegna come la baia di carico fisica verso cui verrà rediretto il pacco. Questa seconda tabella nel database funge da storico delle consegne per ogni singolo pacco e può essere espansa per contenere diverse metriche sulle consegne effettuate. 

### Fase 3

L'ultima fase prevede lo smistamento fisico dei pacchi tramite un nastro trasportatore. Gli attori principali di questa fase sono il driver per attivare il nastro, il sistema di riconoscimento tramite fotocamera e le postazioni di smistamento fisiche, equipaggiate con un servomotore e un sensore di prossimità, che deviano il pacco nella corretta baia di carico. Ogni pacco viene scannerizzato da una fotocamera che ne legge il codice identificativo e, tramite un complicato sistema di specchi e leve, notifica alle postazioni di smistamento l’azione da eseguire: ignorare il pacco o spingerlo verso la baia di carico.

