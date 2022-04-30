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
        solver = Solver(grid)
        solver.click(2, 3)
        solver.print_grid(solver.discovered)
        solution = solver.solve()
        self.assertIsNotNone(solution)
