from unittest import TestCase
from minesweeper import Solver
import json


def read_json_file(file):
    with open(f"../../assets/minesweeper/{file}") as data:
        load = json.load(data)
        return load


class Test(TestCase):

    def test_solve(self):
        grid = read_json_file("example2.json")
        solver = Solver(grid, 2,3)
        solution = solver.solve()
        self.assertIsNotNone(solution)
