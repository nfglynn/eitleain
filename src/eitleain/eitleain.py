import datetime
import time
import aiohttp
import asyncio
import sys
from pathlib import Path
from backports.typing import Dict, List, Optional


class DataPoint(object):
    __slots__ = ["altitude", "speed", "lat", "lon", "track", "time"]

    @classmethod
    def fromDict(cls, data: Dict):
        params = {k: v for (k, v) in data.items() if k in cls.__slots__}
        params["time"] = time.time()
        return cls(**params)

    def __init__(self, altitude, speed, lat, lon, track, time):
        self.altitude = altitude
        self.speed = speed
        self.lat = lat
        self.lon = lon
        self.track = track
        self.time = time

    def __hash__(self):
        return hash((self.altitude,
                     self.speed,
                     self.lat,
                     self.lon,
                     self.track))

    def __eq__(self, other):
        return hash(self) == hash(other)

    @property
    def timestamp(self):
        return time.strftime("%Y/%m/%d %H:%M:%S +0000", time.gmtime(self.time))

    def __str__(self):
        s = "{self.altitude}m {self.speed}kph {self.lat}/{self.lon} {self.track} {self.timestamp}"
        return s.format(self=self)


class Aircraft(object):
    @classmethod
    def fromDict(cls, details: Dict):
        return cls(flight=details['flight'],
                   hex=details['hex'])

    def __init__(self,
                 flight: str,
                 hex: int,
                 data: Optional[List[DataPoint]]=None):
        self.flight = flight.strip() if flight.strip() else None
        self.hex_code = hex
        self.data = data if data is not None else []

    @property
    def id(self) -> str:
        return self.flight if self.flight is not None else str(self.hex_code)

    @property
    def last(self) -> DataPoint:
        return self.data[-1]

    def update(self, data: DataPoint) -> bool:
        if data not in self.data:
            self.data.append(data)
            return True
        return False

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)

    def __repr__(self) -> str:
        return '<{} "{}">'.format(self.__class__.__name__,
                                  str(self))

    def __str__(self) -> str:
        s = "{self.id} {self.last}"
        return s.format(self=self)


class Dump1090(object):
    @property
    def path(self):
        return str(Path('/usr/local/bin/dump1090'))

    @property
    def uri(self):
        return "http://127.0.0.1:8080/data.json"

    def __init__(self):
        self.proc = None

    @asyncio.coroutine
    def get_status(self):
        try:
            response = yield from aiohttp.request('GET', self.uri)
            return (yield from response.read_and_close(decode=True))
        except Exception:
            pass

    @asyncio.coroutine
    def watch(self):
        loop = asyncio.get_event_loop()
        while True:
            for data in loop.run_until_complete(self.get_status()):
                if data is not None:
                    yield (Aircraft.fromDict(data), DataPoint.fromDict(data))


class Speir(object):
    def __init__(self):
        self.radar = Dump1090()
        self.aircraft = {}

    def watch(self):
        for (aircraft, data) in self.radar.watch():
            if aircraft not in self.aircraft:
                self.aircraft[aircraft] = aircraft
            change = self.aircraft[aircraft].update(data)
            if change:
                print(self.aircraft[aircraft])


def main():
    speir = Speir()
    speir.watch()
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
