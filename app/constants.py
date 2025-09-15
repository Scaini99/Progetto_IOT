## Questo file contiene iu file di configurazione per smister.py

## Database
DBHOST="localhost"
DBPORT=5432
DBNAME="centro_smistamento"
DBUSER= "admin"
DBPASSWORD="psqladmin"

## Coordinate della base
BASE_LAT= 45.9558648
BASE_LON= 12.9801816

BASE_COORD=[BASE_LON, BASE_LAT]

NR_OF_VEHICLES= 3

## Nastro trasportatore
PIN_CTRL_CONVEYOR_BELT= 21

## Push station 1
PIN_ECHO_1= 14
PIN_TRIGGER_1= 25  
PIN_SERVO_1= 12 

## Push station 2
PIN_ECHO_2= 15
PIN_TRIGGER_2= 8
PIN_SERVO_2= 13

## Push station 3
PIN_ECHO_3= 18
PIN_TRIGGER_3= 7
PIN_SERVO_3= 16