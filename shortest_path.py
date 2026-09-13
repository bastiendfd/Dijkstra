"""SciPy-backed shortest-path exercise using a small synthetic graph."""

from __future__ import annotations

import argparse
import sys
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
    for name, node in (("start", start), ("end", end)):
        if not 0 <= node < graph.shape[0]:
            raise ValueError(
                f"{name} node must be between 0 and {graph.shape[0] - 1}."
            )

    if (graph.data < 0).any():
        raise ValueError("Dijkstra requires non-negative edge weights.")

    distances, predecessors = dijkstra(
        graph, directed=False, indices=start, return_predecessors=True
    )
    distance = float(distances[end])
    if isinf(distance):
        return None

    nodes = [end]
    visited = {end}
    while nodes[-1] != start:
        predecessor = int(predecessors[nodes[-1]])
        if predecessor in visited:
            raise ValueError("Detected predecessor cycle while reconstructing path.")
        if not 0 <= predecessor < graph.shape[0]:
            raise ValueError("Invalid predecessor while reconstructing path.")
        nodes.append(predecessor)
        visited.add(predecessor)
    nodes.reverse()
    return PathResult(nodes=tuple(nodes), distance=distance)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the sample graph query from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=0, help="start node (default: 0)")
    parser.add_argument("--end", type=int, default=3, help="end node (default: 3)")
    args = parser.parse_args(argv)

    graph = sample_graph()
    for name, node in (("start", args.start), ("end", args.end)):
        if not 0 <= node < graph.shape[0]:
            print(
                f"error: {name} node must be between 0 and {graph.shape[0] - 1}.",
                file=sys.stderr,
            )
            return 2

    result = find_shortest_path(graph, args.start, args.end)
    if result is None:
        print(f"No path from {args.start} to {args.end}.")
    else:
        route = " -> ".join(map(str, result.nodes))
        print(f"Path: {route}")
        print(f"Distance: {result.distance:g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
