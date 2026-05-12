from __future__ import annotations

from astar import astar_search
from dijkstra import dijkstra_search
from grid import create_example_grid
from visualize import generate_visuals


def yes_no(value: bool) -> str:
    return "Yes" if value else "No"


def print_search_results(title: str, result) -> None:
    print(title)
    print(f"Path found: {yes_no(result.path_found)}")
    print(f"Path cost: {result.path_cost}")
    print(f"Nodes explored: {result.nodes_explored}")
    print(f"Path: {result.path}")
    print()


def main() -> None:
    grid = create_example_grid()

    astar_result = astar_search(grid)
    dijkstra_result = dijkstra_search(grid)

    print_search_results("A* Search Results", astar_result)
    print_search_results("Dijkstra Results", dijkstra_result)

    print("Comparison")
    if astar_result.path_cost == dijkstra_result.path_cost:
        print("Both algorithms found the same shortest path cost.")
    else:
        print("The algorithms returned different path costs, so check the implementation.")

    if astar_result.nodes_explored < dijkstra_result.nodes_explored:
        print(
            "A* explored fewer nodes because the Manhattan distance heuristic "
            "guided the search toward the goal."
        )
    else:
        print("On this grid, A* did not explore fewer nodes than Dijkstra.")

    image_paths = generate_visuals(grid, astar_result, dijkstra_result)
    print()
    print("Generated image files:")
    for path in image_paths:
        print(f"- {path}")


if __name__ == "__main__":
    main()
