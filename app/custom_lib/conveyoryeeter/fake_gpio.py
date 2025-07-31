class GPIO:
    BCM = 'BCM'
    OUT = 'OUT'
    IN = 'IN'
    HIGH = 1
    LOW = 0

    @staticmethod
    def setmode(mode):
        print(f"[FAKE GPIO] setmode({mode})")

    @staticmethod
    def setup(pin, mode):
        print(f"[FAKE GPIO] setup(pin={pin}, mode={mode})")

    @staticmethod
    def output(pin, value):
        print(f"[FAKE GPIO] output(pin={pin}, value={value})")

    @staticmethod
    def input(pin):
        print(f"[FAKE GPIO] input(pin={pin})")
        return 0

    @staticmethod
    def cleanup():
        print("[FAKE GPIO] cleanup()")
