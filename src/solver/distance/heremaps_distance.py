from typing import List
import requests
import numpy as np
import math
from src import config
from src.solver.distance.distance_function import DistanceFunction
from src.solver.model.location import Location


class HereMapsDistanceFunction(DistanceFunction):

    @staticmethod
    def generate_region(locations: List[Location]) -> dict:
        if not locations:
            raise ValueError("no locations provided")
        n = len(locations)
        mean_lat = sum([x.lat for x in locations]) / n
        mean_lon = sum([x.lon for x in locations]) / n
        return {
            "type": "circle",
            "center": {"lat": mean_lat, "lon": mean_lon},
            "radius": 50000  # TODO compute a better radius
        }

    @staticmethod
    def generate_body_locations(locations: List[Location]) -> List[dict]:
        return [{"lat": x.lat, "lon": x.lon} for x in locations]

    @staticmethod
    def compute_distances(locations: List[Location]):
        base_url = config.get("HEREMAPS_BASE_URL")
        matrix_url = f'{base_url}/matrix?async=false'
        region = HereMapsDistanceFunction.generate_region(locations)
        body_locations = HereMapsDistanceFunction.generate_body_locations(locations)
        body = {
            "origins": body_locations,
            "region": region
        }
        res = requests.post(matrix_url, data=body, headers={'Content-Type': 'application/json'})
        if not res.status_code == 200:
            raise ValueError("heremaps error")
        json = res.json()
        matrix_ = json['matrix']
        times_ = matrix_['travelTimes']
        np_times = np.array(times_)
        n = len(locations)
        np_times = np_times.reshape((n, n))
        return np_times.tolist()

    @staticmethod
    def compute_distance(a: Location, b: Location) -> float:
        distances = HereMapsDistanceFunction.compute_distances([a, b])
        if not distances or not distances[0]:
            raise ValueError('No distances returned')
        return distances[0][0]


DistanceFunction.register(HereMapsDistanceFunction)

heremaps_distance = HereMapsDistanceFunction()
