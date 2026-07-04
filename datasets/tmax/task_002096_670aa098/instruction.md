You are a mobile build engineer optimizing the artifact caching layer for a massive iOS/Android build pipeline. The cache validity is determined by overlapping timestamp intervals representing valid build epochs. The current naive approach is too slow, causing CI delays.

Your task is to implement an efficient custom interval data structure, verify its correctness using property-based testing, and benchmark its performance.

Please perform the following steps:

1. **Setup**:
   - Create a directory `/home/user/build_cache_optimizer`.
   - Install `pytest` and `hypothesis` (for property-based testing).

2. **Implement the Data Structure**:
   Create `/home/user/build_cache_optimizer/interval_cache.py` containing a Python class `IntervalCache`.
   - The class must maintain a collection of integer intervals.
   - It must have a method `add_interval(start: int, end: int)` where `start <= end`.
   - It must have a method `get_merged_intervals() -> list[tuple[int, int]]`. This method must return a list of merged, non-overlapping intervals sorted by their start times. Overlapping or touching intervals (e.g., `(1, 3)` and `(3, 5)`) must be merged into a single interval (`(1, 5)`).
   - This implementation must be efficient (O(N log N) time complexity for N intervals).

3. **Property-Based Testing**:
   Create `/home/user/build_cache_optimizer/test_properties.py`.
   Use `hypothesis` to generate arbitrary lists of valid intervals (where `start <= end`). Add them to `IntervalCache` and assert the following properties on the output of `get_merged_intervals()`:
   - **Sorted**: The output intervals are strictly sorted by their start times.
   - **Disjoint**: No two consecutive intervals in the output overlap or touch (i.e., `output[i][1] < output[i+1][0]`).
   - **Coverage**: Every original input interval is completely contained within exactly one of the output intervals.
   Ensure this file is discoverable and runnable by `pytest`. Run the tests to ensure your implementation is correct.

4. **Performance Benchmarking**:
   Create `/home/user/build_cache_optimizer/benchmark.py`.
   - In this script, generate exactly 100,000 random intervals.
   - Measure the wall-clock time it takes to instantiate `IntervalCache`, add all 100,000 intervals, and call `get_merged_intervals()`.
   - The script must save the duration to a JSON file at `/home/user/build_cache_optimizer/bench_metrics.json` with the exact format:
     `{"time_seconds": <float>}`
   - Run the benchmark script to generate the JSON file.

Ensure all files are created at the exact paths specified and that your tests and benchmark pass.