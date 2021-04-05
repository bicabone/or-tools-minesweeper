from typing import List

from src import log
from src.solver.distance.distance_function import DistanceFunction
from src.solver.model.location import Location


class ODMatrix:
    def __init__(self, locations: List[Location],
                 distance_function: DistanceFunction,
                 load=False) -> None:
        super().__init__()
        self.locations = locations
        self.distance_function = distance_function
        self.dimension = len(locations)
        self.load = load
        self._matrix = None
        self._init()

    def _init(self):
        log.info(f'Initializing OD matrix of size {self.dimension}^2'
                 f' with {"pre" if self.load else "lazy"}-loading')
        self._matrix = []
        for i in range(self.dimension):
            self._matrix += [[]]
            for j in range(self.dimension):
                self._matrix[i] += [None if i != j else 0]

        if self.load:
            self._matrix = self.distance_function.compute_distances(self.locations)

    def distance(self, i, j) -> float:
        if i == j:
            return 0

        row = self._matrix[i]

        if not row:
            self._matrix[i] = []

        entry = row[j]

        if not entry:
            compute = self._compute(i, j)
            row[j] = compute
            entry = compute

        return entry

    def _compute(self, i, j) -> float:
        return self.distance_function.compute_distance(
            self.locations[i],
            self.locations[j]
        )
