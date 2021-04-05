from unittest import TestCase

from sandbox.distance.pythagorean_distance import PythagoreanDistance
from sandbox.model.location import Location


class TestPythagoreanDistance(TestCase):
    def __init__(self, method_name) -> None:
        super().__init__(method_name)
        self.locations = [
            Location(1, 2),
            Location(1, 3),
            Location(4, 2),
            Location(4, 6)
        ]

    def test_compute_distance(self):
        distance = PythagoreanDistance.compute_distance(self.locations[0], self.locations[3])
        self.assertEqual(5, distance)

    def test_symmetry(self):
        matrix = PythagoreanDistance.compute_distances(self.locations)
        size = len(matrix)
        for i in range(size):
            for j in range(size):
                self.assertEqual(matrix[i][j], matrix[j][i])
