# A* Search Demonstration

This project demonstrates the main idea behind A* search from Hart, Nilsson,
and Raphael's paper, "A Formal Basis for the Heuristic Determination of Minimum
Cost Paths."

The program searches for a shortest path on a 2D grid. Open cells are vertices
of a graph, and legal moves up, down, left, and right are edges with cost 1.
Some cells are obstacles, so the algorithms must route around them.

The project compares:

- **A\***, which uses both the known cost so far and a heuristic estimate.
- **Dijkstra's algorithm**, which uses only the known cost so far.

Both algorithms find the same shortest path cost on this grid, but A* usually
explores fewer nodes because it has extra information about the direction of the
goal.

## The A* Formula

A* chooses which node to explore next using:

```text
f(n) = g(n) + h(n)
```

where:

- `g(n)` is the known cost from the start node to node `n`.
- `h(n)` is the estimated cost from node `n` to the goal.
- `f(n)` is the estimated total cost of a full path through node `n`.

In this project, `h(n)` is the **Manhattan distance**:

```text
abs(current_row - goal_row) + abs(current_col - goal_col)
```

Manhattan distance is a good fit for this grid because movement is only allowed
up, down, left, and right. Diagonal moves are not allowed. Since each move costs
1, Manhattan distance estimates how many grid steps remain if there were no
obstacles in the way.

## Why Compare With Dijkstra?

Dijkstra's algorithm is a classic shortest path algorithm. It always expands the
not-yet-explored node with the smallest known distance from the start.

A* does something similar, but it adds the heuristic estimate. This means A* can
focus more strongly on nodes that appear to lead toward the goal. When the
heuristic is reasonable, A* can find the same optimal path while exploring fewer
nodes.

## Files

- `main.py` runs the demonstration.
- `grid.py` defines the grid, obstacles, start, goal, and Manhattan distance.
- `astar.py` implements A* search from scratch.
- `dijkstra.py` implements Dijkstra's algorithm from scratch.
- `visualize.py` creates the slide-friendly images.
- `requirements.txt` lists the only external dependency.

## How To Run

Install the dependency:

```bash
pip install -r requirements.txt
```

Run the program:

```bash
python main.py
```

The terminal prints the path found by each algorithm, the path cost, and the
number of explored nodes.

## Generated Images

Running `python main.py` creates:

- `grid_initial.png`: the original grid with start, goal, and obstacles.
- `astar_result.png`: A* explored nodes and final path.
- `dijkstra_result.png`: Dijkstra explored nodes and final path.
- `comparison.png`: A* and Dijkstra shown side by side.

In the images:

- `S` is the start.
- `G` is the goal.
- Black cells are obstacles.
- Light blue cells are explored nodes.
- Yellow cells are the final shortest path.

These images are intended to be simple enough to put directly into presentation
slides.
