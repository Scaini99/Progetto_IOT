from typing import List, Dict, Optional
import json

class Vehicle:
    def __init__(self, id, capacity, start: List[float], end: List[float]):
        self.id = id
        self.capacity = [capacity]
        self.start= start
        self.end= end

    def to_dict(self) -> Dict:
        """Converte l'oggetto in un dizionario."""
        return {
            "id": self.id,
            "capacity": self.capacity,
            "start": self.start,
            "end": self.end
        }

    def to_json(self) -> str:
        """Serializza l'oggetto in JSON."""
        return json.dumps(self.to_dict(), indent=2)