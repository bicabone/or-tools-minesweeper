from unittest import TestCase

from src.solver.distance.distance_function import DistanceFunction
from src.solver.model.location import Location


class TestDistanceFunction(TestCase):
    def test_compute_distance(self):
        self.assertRaises(
            ValueError,
            DistanceFunction.compute_distance,
            Location(1, 2),
            Location(3, 4))
