import math
from typing import List

from src.solver.distance.distance_function import DistanceFunction
from src.solver.model.location import Location


class PythagoreanDistance(DistanceFunction):

    @staticmethod
    def compute_distance(a: Location, b: Location) -> float:
        return math.sqrt(
            math.pow(
                a.lat - b.lat, 2
            ) + math.pow(
                a.lon - b.lon, 2
            )
        )

    @staticmethod
    def compute_distances(locations: List[Location]) -> List[List[float]]:
        out = []
        for i in range(len(locations)):
            out += [[]]
            for j in range(len(locations)):
                if i == j:
                    out[i] += [0]
                else:
                    out[i] += [
                        PythagoreanDistance.compute_distance(locations[i], locations[j])]
        return out


DistanceFunction.register(PythagoreanDistance)

pythagorean_distance = PythagoreanDistance()
