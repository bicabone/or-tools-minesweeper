import math
from unittest import TestCase

from sandbox.distance.pythagorean_distance import instance as pythagorean
from sandbox.model.location import Location
from sandbox.distance.od_matrix import ODMatrix


class TestODMatrix(TestCase):

    def __init__(self, method_name) -> None:
        super().__init__(method_name)
        self.locations = [
            Location(1, 2),
            Location(1, 3),
            Location(4, 2)
        ]

    def test__init__is_empty_when_load_is_False(self):
        matrix = ODMatrix(self.locations, pythagorean)
        data = matrix._matrix
        dimension = matrix.dimension
        for i in range(dimension):
            for j in range(dimension):
                entry = data[i][j]
                if i == j:
                    self.assertEqual(0, entry)
                else:
                    self.assertIsNone(entry)

    def test__init__is_not_empty_when_load_is_True(self):
        matrix = ODMatrix(self.locations, pythagorean, load=True)
        data = matrix._matrix
        self.assertEqual(0, data[0][0])
        self.assertEqual(1, data[0][1])
        self.assertEqual(3, data[0][2])
        self.assertEqual(math.sqrt(10), data[1][2])

    def test_diagonal(self):
        matrix = ODMatrix(self.locations, pythagorean)
        for i in range(matrix.dimension):
            self.assertEqual(0, matrix.distance(i, i))

    def test_consistency(self):
        matrix1 = ODMatrix(self.locations, pythagorean, load=False)
        for i in range(matrix1.dimension):
            for j in range(matrix1.dimension):
                matrix1.distance(i, j)
        matrix2 = ODMatrix(self.locations, pythagorean, load=True)
        self.assertEqual(matrix1._matrix, matrix2._matrix)
