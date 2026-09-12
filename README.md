# Shortest-Path Exercise

A small, runnable **SciPy-backed** shortest-path exercise. It demonstrates how to call `scipy.sparse.csgraph.dijkstra` on a synthetic weighted graph and reconstruct a route from SciPy's predecessor output.

> This is not a from-scratch implementation of Dijkstra's algorithm, and it is not presented as production routing software.

## What it demonstrates

- Representing a weighted graph as a SciPy CSR sparse matrix.
- Finding a shortest route between numbered nodes.
- Reporting when a destination is disconnected.
- Running the example from a command line.

The built-in synthetic graph has five nodes. Node `4` is intentionally disconnected. Its shortest route from `0` to `3` is `0 -> 1 -> 2 -> 3`, with total distance `4`.

## Requirements

- Python 3.10 or newer
- `scipy` (installed automatically from the project metadata)

## Run it

Create an environment and install the project:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Run the default query:

```bash
python -m shortest_path
```

Example output:

```text
Path: 0 -> 1 -> 2 -> 3
Distance: 4
```

Choose nodes explicitly, including the disconnected node:

```bash
python -m shortest_path --start 0 --end 4
# No path from 0 to 4.
```

The installed console command is equivalent:

```bash
shortest-path --start 0 --end 3
```

## Test

```bash
python -m pytest
```

The tests cover the known shortest path and a disconnected destination.

## Project layout

- `shortest_path.py` — module and command-line interface.
- `tests/test_shortest_path.py` — executable exercise checks.
- `pyproject.toml` — package, runtime, and test dependencies.

## License

No license has been supplied with this repository. Do not assume permission to reuse it beyond applicable law until the maintainer adds one.
