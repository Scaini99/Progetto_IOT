import json
from typing import List, Dict, Optional
from .job import Job
from .vehicle import Vehicle

class Input:
    def __init__(self):
        self.jobs: List[Job] = []
        self.vehicles: List[Vehicle] = []

    def add_job(self, 
                job: Job
                ):
        """Aggiunge un job (punto da visitare)."""

        self.jobs.append(job)

    def add_vehicle(
        self,
        vehicle: Vehicle
        ):

        self.vehicles.append(vehicle)

    def to_dict(self) -> Dict:
        """Converte l'input in un dizionario per VROOM."""
        return {
            "vehicles": [vehicle.to_dict() for vehicle in self.vehicles],
            "jobs": [job.to_dict() for job in self.jobs],
        }

    def to_json(self) -> str:
        """Esporta l'input come JSON compatibile con VROOM."""
        return json.dumps(self.to_dict(), indent=2)