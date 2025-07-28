# sMister

## Struttura progetto
TODO: da implementare!!

sMister/
├── dockerservices/
│   ├── portainer/
│   │   └── ...
│   ├── database/
│   │   └── ...
│   └── routing/
│       └── ...
└── program/
    ├── custom_lib/
    │   └── ...
    ├── examples/
    │   └── ...
    ├── smister.py
    └── constants.py

NB: gitignore su dockerservices: questa cartella serve solo come root per i servizi docker, è da aggiornare anche nei docker.

## Idea 

L'idea di sMister nasce dalla crescente necessità da parte delle aziende di sistemi automatizzati che rendano più veloce ed efficiente lo smistamento dei pacchi.

## Tecnologie

Per quanto riguarda la piattaforma hardware, si è scelto di utilizzare un Raspberry Pi 5 ovvero un single board computer sufficientemente prestante da supportare un sistema operativo e dotato di pin GPIO utili per il collegamento di componenti esterni. 

Mentre alcuni servizi sono stati delegati a container Docker, il core del progetto è stato sviluppato in Python. Questo linguaggio è stato scelto per via della sua facilità di prototipazione e dell'ampia disponibilità di librerie.

### Servizi Docker

Il sistema è stato reso facilmente configurabile e integrabile in vari ambienti grazie a vari servizi Docker installati in locale.

- Portainer: interfaccia grafica web che permette l'installazione di container in maniera semplificata.
- Grafana: tool di gestione grafica per monitorare le statistiche in tempo reale.
- Postgres: il database che contiene le informazioni relative ai pacchi.
- Adminer: programma che serve per gestire da un interfaccia grafica Postgres.
- VROOM: servizio che fornisce un sistema di routing ottimale. 

I servizi sono stati organizzati in stack dedicati, in modo da raggruppare componenti funzionalmente simili.

## Funzionamento

sMister interroga il database per ottenere l'elenco delle consegne previste e riceve come risposta gli indirizzi dei colli associati. Queste informazioni sono trasformate in jobs, ovvero lavori di consegna da effettuare e, in base alla flotta di veicoli per le consegne disponibili, delega a VROOM il calcolo dei percorsi ottimali per ogni veicolo. 

Una volta calcolato ciò, il sistema deve riconoscere l'id del pacco su un nastro trasportatore per indirizzarlo verso la baia di carico corretta: questo viene fatto tramite un codice a barre che identifica unicamente ogni pacco. Lungo la linea alcuni attuatori si occupano di consegnare alla zona di carico giusta ogni pacco.

## Fasi 

Il sistema funziona in due fasi separate. Durante il primo momento vengono creati i database di supporto contenenti le info per lo smistamento. Durante la seconda fase i pacchi vengono fisicamente smistati.