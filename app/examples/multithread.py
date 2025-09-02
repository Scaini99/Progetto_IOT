import cv2
import threading
import time
from queue import Queue, Empty
from pyzbar import pyzbar

# Funzione del thread che legge i codici QR dalla webcam
def qr_reader(queue: Queue, stop_event: threading.Event):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Errore: impossibile aprire la fotocamera.")
        return

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break

        # Decodifica dei codici QR/barcode
        codes = pyzbar.decode(frame)
        for code in codes:
            data = code.data.decode('utf-8')
            queue.put(data)

        cv2.imshow("Scanner QR/Barcode", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break

    cap.release()
    cv2.destroyAllWindows()

# Funzione del thread che stampa i codici letti
def qr_printer(queue: Queue, stop_event: threading.Event):
    while not stop_event.is_set():
        try:
            code = queue.get(timeout=0.5)
        except Empty:
            continue
        else:
            print("QR letto:", code)

def main():
    queue = Queue()
    stop_event = threading.Event()

    reader_thread = threading.Thread(target=qr_reader, args=(queue, stop_event))
    printer_thread = threading.Thread(target=qr_printer, args=(queue, stop_event))

    reader_thread.start()
    printer_thread.start()

    reader_thread.join()
    printer_thread.join()
    print("Terminato.")

if __name__ == "__main__":
    main()
