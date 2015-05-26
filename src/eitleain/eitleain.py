import time

from .radar import Dump1090
from .aircraft import TrackedAircraft


class Eitleain(object):
    def __init__(self):
        self.radar = Dump1090()
        self.aircraft = {}

    def update(self):
        print('update! {}'.format(time.time()))
        for aircraft_id, data_point in self.radar.scan():
            if aircraft_id in self.aircraft:
                aircraft = self.aircraft[aircraft_id]
            else:
                aircraft = TrackedAircraft(aircraft_id)
                self.aircraft[aircraft_id] = aircraft
            if not aircraft.flight_code and aircraft_id.flight_code:
                aircraft.flight_code = aircraft_id.flight_code
            aircraft.update(data_point)

    def from_flight_code(self, flight_code):
        self.update()
        for aircraft in self.aircraft.values():
            if aircraft.flight_code and aircraft.flight_code == flight_code:
                return aircraft

    def from_hex_code(self, hex_code):
        self.update()
        for aircraft in self.aircraft.values():
            if aircraft.hex_code and aircraft.hex_code == hex_code:
                return aircraft

    @property
    def all(self):
        self.update()
        return list(self.aircraft.values())

    @property
    def recent(self):
        self.update()
        now = time.time()
        return [a for a in self.aircraft.values() if (now - a.last.time) < 60]
