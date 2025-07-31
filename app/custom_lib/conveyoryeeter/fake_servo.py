class FakeServo:
    def __init__(self, pin):
        self.pin = pin
        print(f"[FAKE SERVO] Inizializzato su pin {pin}")

    def min(self):
        print("[FAKE SERVO] → min()")

    def mid(self):
        print("[FAKE SERVO] → mid()")

    def max(self):
        print("[FAKE SERVO] → max()")
