import cv2

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

while True:
    ret, img = cap.read()
    if not ret:
        continue

    data, bbox, _ = detector.detectAndDecode(img)
    if data:
        print("QR Code rilevato:", data)
        ##break

    cv2.imshow("QRCODEscanner", img)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
#------------------------------------------------------------------------------------------------
import cv2
from pyzbar.pyzbar import decode
import psycopg2
import serial
import time

# === CONFIGURAZIONE DB
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "dati_spedizione"
DB_USER = "host"
DB_PASSWORD = "localpassword"

# === CONFIGURAZIONE SERIAL
SERIAL_PORT = "COM3"       # o "/dev/ttyUSB0" su Linux
BAUD_RATE = 9600           # Deve combaciare col microcontrollore

CAMERA_ID = 0
letti = set()
n_pacco = 0
storico = []

# === Inizializza la seriale
try:
    serial_port = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"✅ Porta seriale aperta su {SERIAL_PORT}")
except Exception as e:
    print(f"⚠️ Errore apertura porta seriale: {e}")
    serial_port = None

def get_corriere(tracking_code):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("SELECT corriere FROM spedizioni WHERE tracking_code = %s", (tracking_code,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        return None

def invia_a_corriere(codice):
    if serial_port and serial_port.is_open:
        try:
            serial_port.write(f"{codice}\n".encode())
        except Exception as e:
            return None

def main():
    global n_pacco
    cap = cv2.VideoCapture(CAMERA_ID)
    print("Scanner attivo... premi 'q' per uscire")

    while True:
        success, frame = cap.read()
        if not success:
            continue

        codes = decode(frame)
        for code in codes:
            tracking_code = code.data.decode('utf-8')

            if tracking_code not in letti:
                corriere = get_corriere(tracking_code)
                n_pacco += 1

                if corriere:
                    print(" {n_pacco}° pacco → {tracking_code} → Corriere {corriere}")
                    storico.append((n_pacco, tracking_code, corriere))

                    # invio comando al corriere in tempo reale
                    invia_a_corriere(f"COR{corriere}")
                else:
                    print("{n_pacco}° pacco → {tracking_code} non trovato nel DB.")
                    storico.append((n_pacco, tracking_code, "NON TROVATO"))

                letti.add(tracking_code)
                time.sleep(1.0)

        cv2.imshow("Scanner QR", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print("\n📋 Riepilogo pacchi letti:")
    for numero, codice, corriere in storico:
        print(f"{numero}° pacco → {codice} → Corriere {corriere}")

if __name__ == "__main__":
    main()
