from typing import List, Dict, Optional
import json

class Job:
    def __init__(self, 
    id: int, 
    location:  List[float], 
    service: int= 30
    ):
        self.id= id
        self.location= location
        self.service= service
        self.delivery= [1]

    def to_dict(self) -> Dict:
        """Converte l'oggetto in un dizionario."""
        return {
            "id": self.id,
            "location": self.location,
            "service": self.service,
            "delivery": self.delivery
        }

    def to_json(self) -> str:
        """Serializza l'oggetto in JSON."""
        return json.dumps(self.to_dict(), indent=2)