import cv2

class WatchMyPack:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            raise RuntimeError(f"Impossibile aprire la videocamera con ID {self.camera_id}")
        self.detector = cv2.QRCodeDetector()

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            return frame
        return None

    def read_qr_code(self):
        frame = self.get_frame()
        if frame is not None:
            data, bbox, _ = self.detector.detectAndDecode(frame)
            if data:
                return data
        return None

    def stop(self):
        self.cap.release()
