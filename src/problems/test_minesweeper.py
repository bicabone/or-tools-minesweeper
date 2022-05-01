from unittest import TestCase
from minesweeper import Minesweeper
import json


def read_json_file(file):
    with open(f"../../assets/minesweeper/{file}") as data:
        load = json.load(data)
        return load


class Test(TestCase):

    def test_solve1(self):
        grid = read_json_file("example1.json")
        solver = Minesweeper(grid, 2, 3)
        solution = solver.solve()
        self.assertEqual(solution, [
            [0, 1, 1, 1, 0],
            [0, 1, 'M', 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ])

    def test_solve2(self):
        grid = read_json_file("example2.json")
        solver = Minesweeper(grid, 2, 3)
        solution = solver.solve()
        self.assertEqual(solution, [
            [1, 1, 1, 0, 0, 0, 0],
            [1, 'M', 1, 0, 0, 0, 0],
            [2, 2, 2, 0, 0, 0, 0],
            [1, 'M', 1, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 2, 'M'],
            [0, 1, 1, 2, 'M', 2, 1],
            [0, 1, 'M', 2, 1, 1, 0]
        ])

    def test_solve3(self):
        grid = read_json_file("example3.json")
        solver = Minesweeper(grid)
        solution = solver.solve()
        self.assertEqual(solution, [
            [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
            [1, 2, 1, 1, 0, 1, 'M', 1, 0, 0],
            ['M', 3, 'M', 1, 0, 1, 1, 2, 1, 1],
            [2, 'M', 2, 1, 0, 1, 1, 2, 'M', 2],
            [1, 1, 1, 1, 1, 2, 'M', 2, 2, 'M'],
            [0, 1, 1, 2, 'M', 2, 1, 1, 1, 1],
            [1, 2, 'M', 3, 2, 2, 1, 1, 0, 0],
            ['?', '?', 3, 'M', 2, 2, 'M', 1, 0, 0],
            ['?', '?', '?', 3, 'M', 2, 1, 1, 0, 0],
            ['?', '?', '?', 2, 1, 1, 0, 0, 0, 0]
        ])
