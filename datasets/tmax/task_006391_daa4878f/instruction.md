You are a developer fixing a multi-file Python project used to analyze system compilation metrics. The project is located in `/home/user/metrics_analyzer`.

Currently, the project is failing its test suite because of a broken numerical merging algorithm, and it's missing a crucial mock fixture in the tests.

Your tasks are:

1. **Fix the Algorithm**: Edit `/home/user/metrics_analyzer/analyzer.py`. The function `merge_and_diff(stream_a, stream_b)` takes two lists of tuples: `(timestamp (int), metric_value (float))`. It must return a list of lists `[[timestamp_a, diff], ...]` based on the following rules:
   - Iterate through every point `(ta, va)` in `stream_a`.
   - Find a point `(tb, vb)` in `stream_b` such that the time difference `abs(ta - tb) < 5`.
   - If multiple points in `stream_b` satisfy this, choose the one that minimizes `abs(ta - tb)`.
   - If there is still a tie (e.g., tb is 2 units before and another tb is 2 units after), choose the one with the **smaller** `vb` (metric_value).
   - If a matching point is found in `stream_b`, calculate the absolute difference in values `diff = abs(va - vb)`, rounded to 2 decimal places. Append `[ta, diff]` to the result list.
   - If no point in `stream_b` satisfies the condition, do not include `ta` in the output.

2. **Setup the Mock Fixture**: Edit `/home/user/metrics_analyzer/test_analyzer.py`. Write a test case using `unittest.mock.patch` to mock the `fetch_stream(stream_id)` function from `analyzer`. 
   - When called with `"A"`, it must return `[(10, 100.0), (20, 150.0), (30, 200.0)]`.
   - When called with `"B"`, it must return `[(12, 105.0), (19, 140.0), (35, 210.0)]`.
   - Assert that `process_streams()` returns `[[10, 5.0], [20, 10.0]]`. Ensure the tests pass by running `python3 -m unittest test_analyzer.py`.

3. **Generate Final Output**: Run the provided `main.py` script (`python3 main.py`) which will use your fixed `merge_and_diff` algorithm to process two large streams and output the results to `/home/user/final_diff.json`.

Make sure `/home/user/final_diff.json` is successfully created with the correct JSON array format.