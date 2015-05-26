import json
from pathlib import Path
import requests

from .aircraft import AircraftID, DataPoint


class Dump1090(object):
    @property
    def path(self):
        return str(Path('/usr/local/bin/dump1090'))

    @property
    def uri(self):
        return "http://127.0.0.1:8080/data.json"

    def __init__(self):
        self.proc = None

    def status(self):
        try:
            response = requests.get(self.uri)
            return json.loads(response.text)
        except Exception:
            pass

    def scan(self):
        info = self.status()
        if info is not None:
            for data in info:
                aircraft_id = AircraftID.fromData(data)
                data_point = DataPoint.fromData(data)
                yield (aircraft_id, data_point)
