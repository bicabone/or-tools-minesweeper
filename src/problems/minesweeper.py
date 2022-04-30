from typing import List


class Solver:

    def __init__(self, grid: List[List[str]]) -> None:
        super().__init__()
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        self.discovered = self.create_empty_board()

    def create_empty_board(self) -> List[list]:
        def create_empty_row(width):
            return ["?" for _ in range(width)]

        return [create_empty_row(self.width) for _ in range(self.height)]

    def solve(self):
        print(self.grid)
        return self.grid

    def click(self, i: int, j: int):
        if self.is_mine(i, j):
            self.discovered[i][j] = "M"
            return

        mine_count = self.get_mine_count(i, j)

        self.discovered[i][j] = mine_count

        if mine_count == 0:
            indices = self.neighbor_indices(i, j)
            for index in indices:
                if self.discovered[index[0]][index[1]] == "?":
                    self.click(index[0], index[1])

    def is_mine(self, i, j):
        return self.grid[i][j] == "M"

    def get_mine_count(self, i, j):
        if self.is_mine(i, j):
            return -1

        neighbors = self.neighbor_indices(i, j)
        return sum(1 if self.is_mine(index[0], index[1]) else 0
                   for index in neighbors)

    @staticmethod
    def print_grid(grid):
        [print(*line) for line in grid]

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
