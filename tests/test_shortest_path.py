from scipy.sparse import csr_matrix

from shortest_path import find_shortest_path, sample_graph


def test_finds_known_shortest_path_in_sample_graph():
    result = find_shortest_path(sample_graph(), 0, 3)

    assert result.nodes == (0, 1, 2, 3)
    assert result.distance == 4.0


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
