import pytest
from scipy.sparse import csr_matrix

import shortest_path
from shortest_path import find_shortest_path, main, sample_graph


def test_finds_known_shortest_path_in_sample_graph():
    result = find_shortest_path(sample_graph(), 0, 3)

    assert result.nodes == (0, 1, 2, 3)
    assert result.distance == 4.0


def test_rejects_negative_edge_weights_before_running_dijkstra(monkeypatch):
    graph = csr_matrix(
        [
            [0, -1],
            [-1, 0],
        ],
        dtype=float,
    )

    def dijkstra_must_not_run(*args, **kwargs):
        raise AssertionError("dijkstra must not run for negative weights")

    monkeypatch.setattr(shortest_path, "dijkstra", dijkstra_must_not_run)

    with pytest.raises(ValueError, match="non-negative edge weights"):
        find_shortest_path(graph, 0, 1)


def test_rejects_cyclic_predecessors_during_path_reconstruction(monkeypatch):
    class CyclicPredecessors:
        def __init__(self):
            self.lookups = 0

        def __getitem__(self, node):
            self.lookups += 1
            if self.lookups > 2:
                raise AssertionError("cyclic predecessors were not detected")
            return {1: 2, 2: 1}[node]

    monkeypatch.setattr(
        shortest_path,
        "dijkstra",
        lambda *args, **kwargs: ([0.0, 1.0, 2.0], CyclicPredecessors()),
    )

    with pytest.raises(ValueError, match="predecessor cycle"):
        find_shortest_path(csr_matrix((3, 3)), 0, 1)


@pytest.mark.parametrize(
    ("argv", "expected_error"),
    [
        (["--start", "-1"], "error: start node must be between 0 and 4.\n"),
        (["--end", "5"], "error: end node must be between 0 and 4.\n"),
    ],
)
def test_cli_rejects_out_of_range_nodes(argv, expected_error, capsys):
    assert main(argv) == 2
    assert capsys.readouterr().err == expected_error


def test_returns_no_path_for_disconnected_node():
    graph = csr_matrix(
        [
            [0, 2, 0],
            [2, 0, 0],
            [0, 0, 0],
        ],
        dtype=float,
    )

    result = find_shortest_path(graph, 0, 2)

    assert result is None
