You are an AI assistant helping a data researcher. The researcher is organizing a new text dataset and benchmarking the performance of two different embedding inference methods. 

They have written a Python script `/home/user/benchmark.py` that is supposed to:
1. Load a dataset from `/home/user/dataset.jsonl`.
2. Enforce a strict data schema (ensuring each record has a valid string in the `text` field).
3. Benchmark the inference time of Method A (Sequential) vs Method B (Simulated Batch) for computing embeddings.
4. Perform an independent t-test (hypothesis testing) to compare the mean inference times of the two methods.
5. Save the results to `/home/user/benchmark_results.json`.

However, the script is currently producing an output file with `{"error": "No data"}` (similar to a visualization script producing a blank plot). The researcher suspects there is a flaw in how the data schema enforcement handles malformed rows, causing the entire data pipeline to fail and return an empty array for the benchmarking phase.

Your task:
1. Inspect `/home/user/benchmark.py` and fix the bug so that it correctly skips invalid records (where `text` is not a string) instead of discarding the entire dataset.
2. Run the script so that it processes the dataset, conducts the benchmarking, calculates the p-value from the t-test, and saves the successful output.

The final state must contain a valid `/home/user/benchmark_results.json` with the keys:
- `valid_records_count` (integer)
- `p_value` (float)
- `method_A_mean_time` (float)
- `method_B_mean_time` (float)

All files are located in `/home/user`. You may modify the python script as needed.