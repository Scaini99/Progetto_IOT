#\import cv2

#class WatchMyPack:
#    def __init__(self, camera_id=0):
#        self.camera_id = camera_id
#        self.cap = cv2.VideoCapture(self.camera_id)
#        if not self.cap.isOpened():
#            raise RuntimeError(f"Impossibile aprire la videocamera con ID {self.camera_id}")
 #       self.detector = cv2.QRCodeDetector()
#
#    def get_frame(self):
#        ret, frame = self.cap.read()
#        if ret:
#            return frame
#        return None
#
#    def read_qr_code(self):
#        frame = self.get_frame()
#        if frame is not None:
#           data, bbox, _ = self.detector.detectAndDecode(frame)
#            if data:
#             return data
#      return None

#   def stop(self):
#        self.cap.release()
import cv2 as cv

# Apri webcam
cap = cv.VideoCapture(0)

# Rilevatore QR code
qr_detector = cv.QRCodeDetector()

# Set per memorizzare QR già letti
qr_letti = set()

if not cap.isOpened():
    print("Errore: impossibile aprire la webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Rileva e decodifica QR
    data, bbox, _ = qr_detector.detectAndDecode(frame)

    if data:
        if data not in qr_letti:
            qr_letti.add(data)
            print("QR trovato:", data)
            # Mostra il testo del QR appena rilevato sul video
            cv.putText(frame, data, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostra il video (pulito, senza quadrati persistenti)
    cv.imshow("QR Reader Pulito", frame)

    # ESC per uscire
    if cv.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()