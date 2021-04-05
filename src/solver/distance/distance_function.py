from abc import ABCMeta, ABC, abstractmethod
from typing import List

from src.solver.model.location import Location


class DistanceFunction(ABC, metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def compute_distance(a: Location, b: Location) -> float:
        raise ValueError("Must override base class DistanceFunction")

    @staticmethod
    @abstractmethod
    def compute_distances(locations: List[Location]):
        raise ValueError("Must override base class DistanceFunction")
