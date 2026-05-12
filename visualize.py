from __future__ import annotations

from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap

from grid import Cell, Grid


def draw_grid(
    ax: Axes,
    grid: Grid,
    title: str,
    explored: list[Cell] | None = None,
    path: list[Cell] | None = None,
) -> None:
    explored_set = set(explored or [])
    path_set = set(path or [])

    # 0=open, 1=explored, 2=path, 3=obstacle, 4=start, 5=goal
    values = [[0 for _ in range(grid.width)] for _ in range(grid.height)]

    for row, col in explored_set:
        values[row][col] = 1
    for row, col in path_set:
        values[row][col] = 2
    for row, col in grid.obstacles:
        values[row][col] = 3

    start_row, start_col = grid.start
    goal_row, goal_col = grid.goal
    values[start_row][start_col] = 4
    values[goal_row][goal_col] = 5

    cmap = ListedColormap(
        [
            "#ffffff",  # open
            "#cfe8ff",  # explored
            "#ffcc4d",  # path
            "#111111",  # obstacle
            "#2ca25f",  # start
            "#de2d26",  # goal
        ]
    )

    ax.imshow(values, cmap=cmap, vmin=0, vmax=5)
    ax.set_title(title, fontsize=14, pad=10)
    ax.set_xticks(range(grid.width))
    ax.set_yticks(range(grid.height))
    ax.set_xticklabels(range(grid.width))
    ax.set_yticklabels(range(grid.height))
    ax.set_xticks([x - 0.5 for x in range(1, grid.width)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, grid.height)], minor=True)
    ax.grid(which="minor", color="#777777", linestyle="-", linewidth=0.6)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.tick_params(axis="both", labelsize=8)

    ax.text(
        start_col,
        start_row,
        "S",
        ha="center",
        va="center",
        color="white",
        weight="bold",
        fontsize=12,
    )
    ax.text(
        goal_col,
        goal_row,
        "G",
        ha="center",
        va="center",
        color="white",
        weight="bold",
        fontsize=12,
    )


def add_legend(fig: plt.Figure) -> None:
    legend_items = [
        mpatches.Patch(color="#2ca25f", label="Start"),
        mpatches.Patch(color="#de2d26", label="Goal"),
        mpatches.Patch(color="#111111", label="Obstacle"),
        mpatches.Patch(color="#cfe8ff", label="Explored"),
        mpatches.Patch(color="#ffcc4d", label="Shortest path"),
    ]
    fig.legend(
        handles=legend_items,
        loc="lower center",
        ncol=5,
        frameon=False,
        bbox_to_anchor=(0.5, 0.01),
    )


def save_grid_image(
    grid: Grid,
    filename: str,
    title: str,
    explored: list[Cell] | None = None,
    path: list[Cell] | None = None,
) -> None:
    fig, ax = plt.subplots(figsize=(7, 7))
    draw_grid(ax, grid, title, explored, path)
    add_legend(fig)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(filename, dpi=180)
    plt.close(fig)


def save_comparison_image(
    grid: Grid,
    astar_explored: list[Cell],
    astar_path: list[Cell],
    dijkstra_explored: list[Cell],
    dijkstra_path: list[Cell],
    filename: str = "comparison.png",
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.8))
    draw_grid(axes[0], grid, "A* Search", astar_explored, astar_path)
    draw_grid(axes[1], grid, "Dijkstra's Algorithm", dijkstra_explored, dijkstra_path)
    add_legend(fig)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(filename, dpi=180)
    plt.close(fig)


def generate_visuals(grid: Grid, astar_result, dijkstra_result) -> list[Path]:
    outputs = [
        Path("grid_initial.png"),
        Path("astar_result.png"),
        Path("dijkstra_result.png"),
        Path("comparison.png"),
    ]

    save_grid_image(grid, str(outputs[0]), "Initial Grid")
    save_grid_image(
        grid,
        str(outputs[1]),
        "A* Search Result",
        astar_result.explored_order,
        astar_result.path,
    )
    save_grid_image(
        grid,
        str(outputs[2]),
        "Dijkstra Result",
        dijkstra_result.explored_order,
        dijkstra_result.path,
    )
    save_comparison_image(
        grid,
        astar_result.explored_order,
        astar_result.path,
        dijkstra_result.explored_order,
        dijkstra_result.path,
        str(outputs[3]),
    )

    return outputs
