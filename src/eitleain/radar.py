import json
from pathlib import Path
import requests
import asyncio

from .aircraft import AircraftID, DataPoint


class Dump1090(object):
    @property
    def path(self):
        return str(Path('/usr/local/bin/dump1090'))

    @property
    def uri(self):
        return "http://127.0.0.1:8080/data.json"

    def __init__(self):
        pass

    @asyncio.coroutine
    def status(self):
        try:
            yield from json.loads(requests.get(self.uri).text)
        except Exception:
            pass

    @asyncio.coroutine
    def scan(self):
        while True:
            info = self.status()
            if info is not None:
                for data in info:
                    aircraft_id = AircraftID.fromData(data)
                    data_point = DataPoint.fromData(data)
                    return (aircraft_id, data_point)
            yield from asyncio.sleep(1)
