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
