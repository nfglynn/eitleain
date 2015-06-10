import time
from backports.typing import Dict, Optional, List, Generic, TypeVar


class DataPoint(object):
    __slots__ = ["altitude", "speed", "lat", "lon", "track", "time", "seen"]

    @classmethod
    def fromData(cls, data: Dict):
        params = {k: v for (k, v) in data.items() if k in cls.__slots__}
        params["time"] = time.time()
        return cls(**params)

    def __init__(self, altitude, speed, lat, lon, track, time, seen):
        self.altitude = altitude
        self.speed = speed
        self.lat = lat
        self.lon = lon
        self.track = track
        self.time = time
        self.seen = seen

    def __hash__(self):
        return hash((self.altitude,
                     self.speed,
                     self.lat,
                     self.lon,
                     self.track))
                     #, self.seen))

    def __eq__(self, other):
        return hash(self) == hash(other)

    @property
    def timestamp(self):
        return time.strftime("%Y/%m/%d %H:%M:%S +0000", time.gmtime(self.time))

    def __str__(self):
        s = "{self.altitude}m {self.speed}kph {self.lat}/{self.lon} {self.track} {self.timestamp}"
        return s.format(self=self)

    def as_dict(self):
        return {'speed': self.speed,
                'track': self.track,
                'altitude': self.altitude,
                'lat': self.lat,
                'lon': self.lon,
                'time': self.time,
                'seen': self.seen}


class AircraftID(object):
    @classmethod
    def fromData(cls, data):
        return cls(flight_code=data['flight'],
                   hex_code=data['hex'])

    def __init__(self, flight_code, hex_code):
        self._flight_code = flight_code.strip() if flight_code.strip() else None
        self.hex_code = hex_code

    def __eq__(self, other):
        return self.hex_code == other.hex_code

    def __hash__(self):
        return hash(self.hex_code)

    def __str__(self):
        if self.flight_code is not None:
            return self.flight_code
        else:
            return '[{}]'.format(self.hex_code)

    def __repr__(self):
        return '<{self.__class__.__name__}: {self}>'.format(self=self)

    @property
    def flight_code(self):
        return self._flight_code

    @flight_code.setter
    def flight_code(self, val):
        self._flight_code = val.strip()

    def as_dict(self):
        return {'flight_code': self.flight_code,
                'hex_code': self.hex_code}


class TrackedAircraft(object):
    def __init__(self,
                 aircraft_id: AircraftID,
                 data: Optional[List[DataPoint]]=None):
        self.aircraft_id = aircraft_id
        self.data = data if data is not None else []

    @property
    def flight_code(self):  # -> Optional[str | bool]:
        return self.aircraft_id.flight_code

    @flight_code.setter
    def flight_code(self, flight_code):
        if self.flight_code is not None:
            m = "Can't set flight_code: {} -> {}"
            raise Exception(m.format(self.flight_code,
                                     flight_code))
        self.aircraft_id.flight_code = flight_code

    @property
    def last(self) -> DataPoint:
        return self.data[-1]

    def update(self, data: DataPoint) -> bool:
        if data not in self.data:
            self.data.append(data)
            return True
        return False

    def __hash__(self):
        return hash(self.aircraft_id)

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)

    def __repr__(self) -> str:
        return '<{} "{}">'.format(self.__class__.__name__,
                                  str(self))

    def __str__(self) -> str:
        s = "{self.aircraft_id} {self.last}"
        return s.format(self=self)

    def as_dict(self, history=None):
        details = (self.aircraft_id.as_dict())
        if history is False:
            details['data'] = [self.last.as_dict()]
        elif history is True:
            details['data'] = [d.as_dict() for d in reversed(self.data)]
        return details
