from __future__ import annotations

import heapq
from dataclasses import dataclass
from math import inf

from grid import Cell, Grid, manhattan_distance


@dataclass(frozen=True)
class SearchResult:
    path_found: bool
    path: list[Cell]
    path_cost: int | None
    nodes_explored: int
    explored_order: list[Cell]
    g_scores: dict[Cell, int]
    h_scores: dict[Cell, int]
    f_scores: dict[Cell, int]


def reconstruct_path(came_from: dict[Cell, Cell], start: Cell, goal: Cell) -> list[Cell]:
    path = [goal]
    current = goal

    while current != start:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path


def astar_search(grid: Grid) -> SearchResult:
    """Run A* search with f(n) = g(n) + h(n).

    The heap stores (f, h, counter, cell). Including h as the second field means
    ties on f are broken by preferring the node closer to the goal.
    """

    start = grid.start
    goal = grid.goal

    open_heap: list[tuple[int, int, int, Cell]] = []
    counter = 0

    start_h = manhattan_distance(start, goal)
    g_scores: dict[Cell, int] = {start: 0}
    h_scores: dict[Cell, int] = {start: start_h}
    f_scores: dict[Cell, int] = {start: start_h}
    came_from: dict[Cell, Cell] = {}
    closed: set[Cell] = set()
    explored_order: list[Cell] = []

    heapq.heappush(open_heap, (start_h, start_h, counter, start))

    while open_heap:
        _, _, _, current = heapq.heappop(open_heap)

        if current in closed:
            continue

        closed.add(current)
        explored_order.append(current)

        if current == goal:
            path = reconstruct_path(came_from, start, goal)
            return SearchResult(
                path_found=True,
                path=path,
                path_cost=g_scores[goal],
                nodes_explored=len(explored_order),
                explored_order=explored_order,
                g_scores=g_scores,
                h_scores=h_scores,
                f_scores=f_scores,
            )

        for neighbor in grid.neighbors(current):
            if neighbor in closed:
                continue

            tentative_g = g_scores[current] + 1
            if tentative_g < g_scores.get(neighbor, inf):
                came_from[neighbor] = current
                h = manhattan_distance(neighbor, goal)
                f = tentative_g + h

                g_scores[neighbor] = tentative_g
                h_scores[neighbor] = h
                f_scores[neighbor] = f

                counter += 1
                heapq.heappush(open_heap, (f, h, counter, neighbor))

    return SearchResult(
        path_found=False,
        path=[],
        path_cost=None,
        nodes_explored=len(explored_order),
        explored_order=explored_order,
        g_scores=g_scores,
        h_scores=h_scores,
        f_scores=f_scores,
    )
