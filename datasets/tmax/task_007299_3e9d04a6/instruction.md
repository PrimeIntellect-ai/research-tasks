You are a backend web developer building a high-performance delivery pricing feature for a local commerce platform. The platform has thousands of "delivery anchors" (represented as 2D coordinates), and when a customer requests a delivery at a specific coordinate, we need to quickly find the minimum delivery cost among all anchors within a specific radius.

Your task is to implement a custom spatial data structure, parse existing anchor data, benchmark your solution against a naive approach, and write unit tests.

Here are your requirements:

1. **Custom Data Structure (`/home/user/spatial_grid.py`)**
Write a Python module containing a class `DeliveryGrid`. The naive $O(N)$ approach of checking every anchor for every query is too slow. You must implement a spatial grid (or spatial hash) to achieve $O(1)$ or $O(\log N)$ average query time.
The class must have:
- `__init__(self, cell_size: float)`: Initializes the grid. Use a cell size to bin coordinates.
- `insert(self, x: float, y: float, base_cost: float, multiplier: float)`: Adds a delivery anchor to the grid.
- `query_min_cost(self, qx: float, qy: float, radius: float) -> float`: Finds all anchors strictly within or exactly on the `radius` from `(qx, qy)` using Euclidean distance. 
  For each anchor within the radius, calculate the cost: `Cost = base_cost + (multiplier * distance)`.
  Return the minimum cost among these anchors, rounded to exactly 2 decimal places. If no anchors are within the radius, return `-1.0`.

2. **Parsing and Execution (`/home/user/run_queries.py`)**
There is a file `/home/user/delivery_zones.json` containing a list of dictionaries: `[{"x": float, "y": float, "base_cost": float, "multiplier": float}, ...]`.
There is another file `/home/user/queries.json` containing a list of queries: `[{"qx": float, "qy": float, "radius": float}, ...]`.
Write a script that:
- Loads the zones and inserts them into a `DeliveryGrid` with `cell_size = 10.0`.
- Processes each query from `queries.json` in order.
- Saves a JSON array of the resulting minimum costs (floats) to `/home/user/query_results.json`.

3. **Performance Benchmarking (`/home/user/benchmark.py`)**
Write a script that benchmarks your `DeliveryGrid` `query_min_cost` against a naive function that simply iterates over a flat list of all anchors.
- Measure the total time to run all queries in `queries.json` using the naive approach.
- Measure the total time to run all queries using your `DeliveryGrid`.
- Output a JSON file at `/home/user/benchmark_results.json` with the format: `{"naive_time_sec": float, "grid_time_sec": float, "speedup": float}` (where speedup is naive / grid).

4. **Testing (`/home/user/test_spatial_grid.py`)**
Write a `pytest` test file that tests the `DeliveryGrid` with at least 3 distinct test cases (e.g., exact matches, out of bounds, multiple items in range). You must install `pytest` via pip and run the tests to ensure they pass.

Note: You can use standard library modules (like `math`, `json`, `time`) and `pytest`. Ensure floating-point distance comparisons use standard `math.hypot` or `math.sqrt` to avoid discrepancies.