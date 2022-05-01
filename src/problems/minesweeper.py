from typing import List
from ortools.linear_solver import pywraplp as ot


class Solver:

    def __init__(self, data: List[List[str]], i, j) -> None:
        super().__init__()
        self.data = data
        self.height = len(data)
        self.width = len(data[0])
        self.board = self.create_empty_board()  # type: List[List[int or str]]
        self.print_grid(self.board)
        self.total = self.total_mines()
        self.solver, self.variables = self.create_solver()
        self.click(i, j)
        self.add_constraints()

    def create_empty_board(self) -> List[List[int or str]]:
        def create_empty_row(width):
            return ["?" for _ in range(width)]

        return [create_empty_row(self.width) for _ in range(self.height)]

    def create_solver(self):
        solver = ot.Solver.CreateSolver('GLOP')
        variables = [
            [solver.NumVar(0, 1, f"({i},{j})") for j in range(self.width)]
            for i in range(self.height)
        ]
        return solver, variables

    def add_constraints(self):
        # Add total constraint
        self.print_grid(self.board)
        all_entries = [x for y in self.variables for x in y]
        self.solver.Add(sum(all_entries) == self.total)

        # Add zeros
        zeroes = [self.variables[i][j]
                  for j in range(self.width)
                  for i in range(self.height)
                  if type(self.board[i][j]) == int]
        for zero in zeroes:
            self.solver.Add(zero == 0)

        # Add mines
        mines = [self.variables[i][j]
                 for j in range(self.width)
                 for i in range(self.height)
                 if type(self.board[i][j]) == str and self.board[i][j] == "M"]
        for mine in mines:
            self.solver.Add(mine == 1)

        # Add borders
        border = self.get_border()
        for entry in border:
            i, j = entry[0], entry[1]
            value = self.board[i][j]
            neighbors = self.neighbor_indices(i, j)
            neighbor_vars = [self.variables[n[0]][n[1]] for n in neighbors]
            self.solver.Add(sum(neighbor_vars) == value)

    def solve(self):
        while self.total_unvisited() > self.total:
            max_boarder = {entry: self.maximize(entry[0], entry[1]) for entry in self.get_unknown_border()}
            for index, _max in max_boarder.items():
                if _max == 0:
                    self.click(index[0], index[1])

            min_boarder = {entry: self.minimize(entry[0], entry[1]) for entry in self.get_unknown_border()}
            for index, _min in min_boarder.items():
                if _min == 1:
                    self.board[index[0]][index[1]] = "M"

            self.solver, self.variables = self.create_solver()
            self.add_constraints()

        return self.board

    def total_unvisited(self):
        return sum(self.board[i][j] in ["?", "M"] for i in range(self.height) for j in range(self.height))

    def total_mines(self):
        return sum(self.data[i][j] == "M" for i in range(self.height) for j in range(self.height))

    def click(self, x, y):
        def _click(i: int, j: int):
            if self.is_mine(i, j):
                self.board[i][j] = "💣"
                raise ValueError("Hit a mine!")

            mine_count = self.get_mine_count(i, j)

            self.board[i][j] = mine_count

            if mine_count == 0:
                indices = self.neighbor_indices(i, j)
                for index in indices:
                    if self.board[index[0]][index[1]] == "?":
                        _click(index[0], index[1])

        _click(x, y)

    def maximize(self, i, j):
        variable = self.variables[i][j]
        self.solver.Maximize(variable)
        self.solver.Solve()
        value = self.solver.Objective().Value()
        return int(value)

    def minimize(self, i, j):
        variable = self.variables[i][j]
        self.solver.Minimize(variable)
        self.solver.Solve()
        value = self.solver.Objective().Value()
        return value

    def is_mine(self, i, j):
        return self.data[i][j] == "M"

    def get_mine_count(self, i, j):
        if self.is_mine(i, j):
            return -1

        neighbors = self.neighbor_indices(i, j)
        return sum(1 if self.is_mine(index[0], index[1]) else 0
                   for index in neighbors)

    def get_border(self):
        def match(a, b):
            element = self.board[a][b]
            if type(element) != int or element == 0:
                return False
            indices = self.neighbor_indices(a, b)
            for index in indices:
                entry = self.board[index[0]][index[1]]
                if entry in ['?', "M"]:
                    return True
            return False

        return [(i, j)
                for i in range(self.height)
                for j in range(self.width)
                if match(i, j)]

    def get_unknown_border(self):
        def match(a, b):
            if self.board[a][b] != '?':
                return False
            indices = self.neighbor_indices(a, b)
            for index in indices:
                entry = self.board[index[0]][index[1]]
                if type(entry) == int and entry > 0:
                    return True
            return False

        return [(i, j)
                for i in range(self.height)
                for j in range(self.width)
                if match(i, j)]

    @staticmethod
    def print_grid(grid):
        [print(*line) for line in grid]
        print()

    def neighbor_indices(self, i, j):
        """clockwise"""
        valid_indices = []

        # NW
        if i > 0 and j > 0:
            valid_indices.append((i - 1, j - 1))

        # N
        if i > 0:
            valid_indices.append((i - 1, j))

        # NE
        if i > 0 and j < self.width - 1:
            valid_indices.append((i - 1, j + 1))

        # E
        if j < self.width - 1:
            valid_indices.append((i, j + 1))

        # SE
        if i < self.height - 1 and j < self.width - 1:
            valid_indices.append((i + 1, j + 1))

        # S
        if i < self.height - 1:
            valid_indices.append((i + 1, j))

        # SW
        if i < self.height - 1 and j > 0:
            valid_indices.append((i + 1, j - 1))

        # W
        if j > 0:
            valid_indices.append((i, j - 1))

        return valid_indices
