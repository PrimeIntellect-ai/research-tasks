You are an MLOps engineer responsible for setting up an inference tracking environment and cleaning a repository of historical experiment artifacts.

Your task has two main parts:

Part 1: Fix and Benchmark the Inference Tracker
We use a custom, lightweight C++ library for logging inference metrics, located at `/app/libinfer_ops-1.2.0`. 
1. The library is currently failing to compile due to a configuration or code perturbation in the vendored source. Diagnose and fix the issue so that it compiles successfully using `make`.
2. Once compiled, run the generated `./benchmark_infer` binary. This tool benchmarks the tracking overhead. It will output a file named `baseline_perf.txt` in the `/app/libinfer_ops-1.2.0` directory. Leave this file in place.

Part 2: Build the Artifact Sanitizer
We have a large collection of historical experiment artifacts (CSV files containing inference latencies in milliseconds). Some of these artifacts are corrupted due to bad sensor reads or system hangs (containing excessive missing values or extreme outliers).
You must write a C++ program at `/home/user/sanitizer.cpp` and compile it to `/home/user/sanitizer`.

The `sanitizer` must accept a single argument: the path to a CSV file.
It must parse the file (which contains a single column of floating-point latency values, with a header `latency_ms`) and perform the following operations:
1. Missing Value Handling: Identify and discard any invalid records. Missing or corrupted latencies are recorded as either `NaN` or negative values (e.g., `-1.0`). If more than 20% of the total rows in the file are invalid, the program must reject the file immediately (exit with status code 1).
2. Outlier Detection via Bootstrapping: For the remaining valid latencies, use bootstrap sampling (1,000 resamples with replacement) to estimate the mean latency. Calculate the 95% confidence interval (using the 2.5th and 97.5th percentiles of the bootstrap distribution).
3. Rejection Criterion: If the upper bound of the 95% confidence interval exceeds 100.0 ms, the artifact is considered corrupted by outliers and must be rejected (exit with status code 1).
4. Acceptance: If the file passes both checks, it is a valid artifact (exit with status code 0).

Your compiled binary must be executable as:
`/home/user/sanitizer <path_to_csv>`

Ensure your program is efficient, strictly uses the standard library (`<iostream>`, `<fstream>`, `<vector>`, `<cmath>`, `<random>`, `<algorithm>`, etc.), and handles standard edge cases for file reading.