"""SciPy-backed shortest-path exercise using a small synthetic graph."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import isinf
from typing import Sequence

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra


@dataclass(frozen=True)
class PathResult:
    """The total distance and nodes of one shortest route."""

    nodes: tuple[int, ...]
    distance: float


def sample_graph() -> csr_matrix:
    """Return a small undirected weighted graph with node 4 disconnected."""
    return csr_matrix(
        [
            [0, 1, 5, 0, 0],
            [1, 0, 2, 5, 0],
            [5, 2, 0, 1, 0],
            [0, 5, 1, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        dtype=float,
    )


def find_shortest_path(graph: csr_matrix, start: int, end: int) -> PathResult | None:
    """Find one shortest path with SciPy, or return ``None`` if unreachable."""
    distances, predecessors = dijkstra(
        graph, directed=False, indices=start, return_predecessors=True
    )
    distance = float(distances[end])
    if isinf(distance):
        return None

    nodes = [end]
    while nodes[-1] != start:
        nodes.append(int(predecessors[nodes[-1]]))
    nodes.reverse()
    return PathResult(nodes=tuple(nodes), distance=distance)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the sample graph query from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=0, help="start node (default: 0)")
    parser.add_argument("--end", type=int, default=3, help="end node (default: 3)")
    args = parser.parse_args(argv)

    result = find_shortest_path(sample_graph(), args.start, args.end)
    if result is None:
        print(f"No path from {args.start} to {args.end}.")
    else:
        route = " -> ".join(map(str, result.nodes))
        print(f"Path: {route}")
        print(f"Distance: {result.distance:g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
