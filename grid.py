from __future__ import annotations

from dataclasses import dataclass


Cell = tuple[int, int]


@dataclass(frozen=True)
class Grid:
    """A rectangular grid graph with blocked obstacle cells."""

    width: int
    height: int
    start: Cell
    goal: Cell
    obstacles: set[Cell]

    def in_bounds(self, cell: Cell) -> bool:
        row, col = cell
        return 0 <= row < self.height and 0 <= col < self.width

    def is_open(self, cell: Cell) -> bool:
        return self.in_bounds(cell) and cell not in self.obstacles

    def neighbors(self, cell: Cell) -> list[Cell]:
        row, col = cell
        candidates = [
            (row - 1, col),  # up
            (row + 1, col),  # down
            (row, col - 1),  # left
            (row, col + 1),  # right
        ]
        return [neighbor for neighbor in candidates if self.is_open(neighbor)]


def manhattan_distance(a: Cell, b: Cell) -> int:
    """Distance on a grid when only up/down/left/right moves are allowed."""

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def create_example_grid() -> Grid:
    """Create a fixed 12x12 grid for the classroom demonstration.

    The obstacles leave a winding route to the goal. A* and Dijkstra both find
    the same minimum-cost path, but A* explores less of the grid because the
    Manhattan heuristic points the search toward the lower-right goal.
    """

    obstacles = {
        (0, 4),
        (1, 1),
        (1, 2),
        (1, 4),
        (1, 7),
        (1, 8),
        (1, 9),
        (2, 4),
        (2, 7),
        (3, 1),
        (3, 2),
        (3, 4),
        (3, 5),
        (3, 7),
        (3, 10),
        (4, 5),
        (4, 7),
        (4, 10),
        (5, 0),
        (5, 1),
        (5, 2),
        (5, 5),
        (5, 7),
        (5, 8),
        (5, 10),
        (6, 5),
        (6, 10),
        (7, 2),
        (7, 3),
        (7, 4),
        (7, 5),
        (7, 7),
        (7, 8),
        (7, 10),
        (8, 7),
        (8, 10),
        (9, 1),
        (9, 2),
        (9, 3),
        (9, 7),
        (9, 10),
        (10, 3),
        (10, 5),
        (10, 6),
        (10, 7),
    }

    return Grid(
        width=12,
        height=12,
        start=(0, 0),
        goal=(11, 11),
        obstacles=obstacles,
    )
