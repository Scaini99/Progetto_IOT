from custom_lib.conveyoryeeter import watchmypack

### init camera
camera= watchmypack.WatchMyPack()

while tot_packages > 0:

    frame = camera.get_frame()

    if frame is not None:
        # qui puoi fare l'elaborazione, tipo riconoscere ID
        id = 1001  # esempio placeholder
        print("Frame letto, ID:", id)

    loading_bay= 1 # selectfrom"table" la loadingbay dedicata, potevamo farlo senza scomodare il db? si. sarebbe stato piu' efficente? si. ho voglia di implementarlo ora? no, il db fa figo

    if id!= None:
        print(id)
        for i in range(loading_bay):
            sorting_station= sorting_stations[i]

            if i < loading_bay:
                sorting_station.enqueue(False)
            if i == loading_bay :
                sorting_station.enqueue(True)
            else:
               print("err") 

    ## ora controlliamo le postazioni varie per vedere se c'e' un pacco davanti
    for i in range(nr_postazioni):
        sorting_station= sorting_stations[i]

        if sorting_station.is_passing():
            azione= sorting_station.dequeue()
            if azione == True:
                sorting_station.push_package()
    tot_packages=0## eliminami poi

"""
pseudo:

    QUESTO PSEUDO E' DA CONTROLLARE PER SPUNTI FUTURI, ORA E' UN PO OUTDATED
    /*inizializzate in constants*/
    LIST_ECHO_PINS
    LIST_TRIGGER_PINS
    LIST_SERVO_PINS

    conveyorsistem(conveypinengine)

    nr_postazioni= NR_OF_VEHICLES
    
    // aggiunge sortingstations al sistema di smistamento
    for i in 1..nr_postazioni{
        sortingstation= New Sortingstation(i, LIST_TRIGGER_PIN[i], LIST_ECHO_PIN[i], LIST_SERVO_PINS[i])
        conveyorsistem.add_sortingstation(sortingstation)
    }

    // costruito il sistema di smistamento

    while pacchi_da_smistare > 0{

        id= scannerizza_fotocamera()

        // già, non sto parallelizzado, sono proprio un marpione
        // cmq
        // se la fotocamera legge un valore, aggiorna le relative postazioni di smistamento
        if id!= null{
            for i in 1..id{
                // funziona se passato by reference
                sortingstation= conveyorsistem.get_sortingstation(i)

                if i < id {
                    sortingstation.enqueue(False)
                }if i == id {
                    sortingstation.enqueue(True)
                }else {
                    //errore... 
                }

            }
        }

        // le postazioni controllano se gli passa un pacco davanti
        for i in 1..nr_postazioni{
            postazione= coveyorsystem.get_sortingstation(i)

            if postazione.is_passing(){
                azione= postazione.dequeue()

                if azione == True{
                    postazione.push_package()
                }
            }
        }
        
    }
"""
