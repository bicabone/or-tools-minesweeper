from typing import List

from src.solver.distance.heremaps_distance import heremaps_distance
from src.solver.distance.od_matrix import ODMatrix
from src.solver.model.location import Location


class HereMapsODMatrix(ODMatrix):

    def __init__(self, locations: List[Location], load=False) -> None:
        super().__init__(locations, heremaps_distance, load)


