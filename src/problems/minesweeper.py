from typing import List, Tuple
from ortools.linear_solver import pywraplp as ot
from simple_chalk import chalk


class Minesweeper:
    UNKNOWN = "?"
    MINE = "M"

    def __init__(self, data: List[List[str]], i=0, j=0) -> None:
        super().__init__()
        self.minefield = data
        self.starting_point = (i, j)
        self.last_click = self.starting_point
        self.height = len(data)
        self.width = len(data[0])
        self.solvable = True
        self.board = Minesweeper.create_empty_board(self.height, self.width)
        self.total = self.total_mines()
        self.solver, self.variables = self.create_solver(self.height, self.width)

    def solve(self):
        self.click(self.starting_point)

        while self.total_unvisited() > self.total:
            self.add_constraints()
            action = False

            unknown_boarder = self.get_unknown_border()
            max_boarder = {entry: self.maximize(entry) for entry in unknown_boarder}
            for index, _max in max_boarder.items():
                if _max == 0:
                    self.click(index)
                    action = True

            min_boarder = {entry: self.minimize(entry) for entry in unknown_boarder}
            for index, _min in min_boarder.items():
                if _min == 1:
                    i, j = index
                    self.board[i][j] = Minesweeper.MINE
                    action = True

            if not action:
                self.solvable = False
                break

        self.last_click = None
        self.print_grid()
        if not self.solvable:
            print(chalk.redBright("Unsolvable."))
        return self.board

    @classmethod
    def create_empty_board(cls, height, width) -> List[List[int or str]]:
        def create_empty_row():
            return ["?" for _ in range(width)]

        return [create_empty_row() for _ in range(height)]

    @classmethod
    def create_solver(cls, height, width):
        def create_var(x, y):
            return solver.NumVar(0, 1, f"({x},{y})")

        solver = ot.Solver.CreateSolver('GLOP')
        variables = [[create_var(i, j) for j in range(width)] for i in range(height)]
        return solver, variables

    def add_constraints(self):
        # Add total constraint
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
                 if type(self.board[i][j]) == str and self.board[i][j] == Minesweeper.MINE]
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

    def total_unvisited(self):
        return sum(self.board[i][j] in [Minesweeper.UNKNOWN, Minesweeper.MINE] for i in range(self.height) for j in
                   range(self.height))

    def total_mines(self):
        return sum(self.minefield[i][j] == Minesweeper.MINE for i in range(self.height) for j in range(self.height))

    def click(self, index):
        self.last_click = index
        self.print_grid()

        def _click(idx: Tuple[int, int]):
            i, j = idx
            if self.is_mine(idx):
                self.board[i][j] = "💣"
                raise ValueError("Hit a mine!")

            mine_count = self.get_mine_count(i, j)

            self.board[i][j] = mine_count

            if mine_count == 0:
                indices = self.neighbor_indices(i, j)
                for index_ in (i for i in indices if self.board[i[0]][i[1]] == Minesweeper.UNKNOWN):
                    _click(index_)

        _click(index)

    def maximize(self, entry):
        i, j = entry
        variable = self.variables[i][j]
        self.solver.Maximize(variable)
        self.solver.Solve()
        value = self.solver.Objective().Value()
        return int(value)

    def minimize(self, entry):
        i, j = entry
        variable = self.variables[i][j]
        self.solver.Minimize(variable)
        self.solver.Solve()
        value = self.solver.Objective().Value()
        return value

    def is_mine(self, index):
        i, j = index
        return self.minefield[i][j] == Minesweeper.MINE

    def get_mine_count(self, i, j):
        if self.is_mine((i, j)):
            return -1

        neighbors = self.neighbor_indices(i, j)
        return sum(self.is_mine(index) for index in neighbors)

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
                i, j = index
                entry = self.board[i][j]
                if type(entry) == int:
                    return True
            return False

        return [(i, j)
                for i in range(self.height)
                for j in range(self.width)
                if match(i, j)]

    def print_grid(self, grid=None):
        last_click = self.last_click

        def color(i, line):
            def color_(j, item):
                if (i, j) == last_click:
                    return chalk.green.bold(item)
                if item == Minesweeper.MINE:
                    return chalk.redBright(item)
                if type(item) == int and item > 0:
                    return chalk.blue.bold(item)
                if type(item) == int and item == 0:
                    return chalk.blackBright(item)
                if item == Minesweeper.UNKNOWN:
                    return chalk.whiteBright(item)
                return item

            return [color_(j, x) for j, x in enumerate(line)]

        grid = grid if grid else self.board
        [print(*color(i, line)) for i, line in enumerate(grid)]
        print()

    def neighbor_indices(self, i, j):
        def make_index(di, dj):
            index = (i + di, j + dj)
            return index if 0 <= index[0] <= self.height - 1 and 0 <= index[1] <= self.height - 1 else None

        return [index for index in [
            make_index(delta_i, delta_j)
            for delta_i in [-1, 0, 1]
            for delta_j in [-1, 0, 1]
        ] if index]
