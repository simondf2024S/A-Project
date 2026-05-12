from __future__ import annotations

import heapq
from dataclasses import dataclass
from math import inf

from grid import Cell, Grid


@dataclass(frozen=True)
class DijkstraResult:
    path_found: bool
    path: list[Cell]
    path_cost: int | None
    nodes_explored: int
    explored_order: list[Cell]
    distances: dict[Cell, int]


def reconstruct_path(came_from: dict[Cell, Cell], start: Cell, goal: Cell) -> list[Cell]:
    path = [goal]
    current = goal

    while current != start:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path


def dijkstra_search(grid: Grid) -> DijkstraResult:
    """Run Dijkstra's algorithm on the same grid graph.

    This is equivalent to A* with h(n) = 0 for every node, so the search expands
    outward by known distance from the start instead of aiming at the goal.
    """

    start = grid.start
    goal = grid.goal

    priority_queue: list[tuple[int, int, Cell]] = []
    counter = 0
    distances: dict[Cell, int] = {start: 0}
    came_from: dict[Cell, Cell] = {}
    closed: set[Cell] = set()
    explored_order: list[Cell] = []

    heapq.heappush(priority_queue, (0, counter, start))

    while priority_queue:
        current_distance, _, current = heapq.heappop(priority_queue)

        if current in closed:
            continue

        closed.add(current)
        explored_order.append(current)

        if current == goal:
            path = reconstruct_path(came_from, start, goal)
            return DijkstraResult(
                path_found=True,
                path=path,
                path_cost=current_distance,
                nodes_explored=len(explored_order),
                explored_order=explored_order,
                distances=distances,
            )

        for neighbor in grid.neighbors(current):
            if neighbor in closed:
                continue

            new_distance = current_distance + 1
            if new_distance < distances.get(neighbor, inf):
                distances[neighbor] = new_distance
                came_from[neighbor] = current
                counter += 1
                heapq.heappush(priority_queue, (new_distance, counter, neighbor))

    return DijkstraResult(
        path_found=False,
        path=[],
        path_cost=None,
        nodes_explored=len(explored_order),
        explored_order=explored_order,
        distances=distances,
    )
