import asyncio
import sys
import os
import json
from pathlib import Path

SRC_PATH = Path(os.path.normpath(os.path.join(os.path.abspath(__file__),
                                              os.path.pardir,
                                              os.path.pardir)))

sys.path.insert(1, str(SRC_PATH))

from flask import Flask, request, render_template
from flask_restful import Resource, Api, fields, marshal_with
from werkzeug.routing import BaseConverter

from eitleain import Eitleain

app = Flask(__name__)
api = Api(app)

eitleain = Eitleain()


class AircraftConverter(BaseConverter):
    def to_python(self, value):
        aircraft_name = value.strip()
        if aircraft_name and aircraft_name[0].isalpha():
            # assume a flight code
            aircraft = eitleain.from_flight_code(aircraft_name)
        else:
            # assume a hex code
            aircraft = eitleain.from_hex_code(aircraft_name)
        if aircraft is not None:
            return aircraft
        else:
            import ipdb; ipdb.set_trace()
            raise Exception("Unknown Flight {}".format(aircraft_name))

    def to_url(self, aircraft):
        return '+'.join(BaseConverter.to_url(str(a))
                        for a in aircraft)


app.url_map.converters['aircraft'] = AircraftConverter


class AircraftList(Resource):
    def get(self, method):
        if method == 'all':
            return [a.as_dict(history=False) for a in eitleain.all]
        elif method == 'recent':
            return [a.as_dict(history=False) for a in eitleain.recent]
        else:
            return render_template('error.html'), 404


class AircraftDetails(Resource):
    def get(self, aircraft):
        return aircraft.as_dict(history=True)


api.add_resource(AircraftList, '/speir/<string:method>')
api.add_resource(AircraftDetails, '/details/<aircraft:aircraft>')


if __name__ == '__main__':
    app.run(debug=True)
