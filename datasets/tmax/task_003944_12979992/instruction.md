You are acting as a log analyst investigating server performance patterns. We have a massive JSONL log file at `/home/user/server_logs.jsonl`. We previously wrote a Python script (`/app/baseline.py`) to process these logs, filter them, and compute summary statistics. However, the Python script is far too slow for our production data volume.

We have decided to rewrite the log analyzer in C++ using the ultra-fast `simdjson` library. 

Your tasks are as follows:
1. We have downloaded the `simdjson` source code to `/app/simdjson`. A build script for our new C++ tool is located at `/app/build.sh`, but it currently fails to compile because of an incorrect compiler configuration. Diagnose and fix `/app/build.sh`.
2. Write a C++ program at `/home/user/analyzer.cpp` that does the following:
   - Reads the JSON Lines file `/home/user/server_logs.jsonl`.
   - Parses each line using the vendored `simdjson` library (the single-header version is at `/app/simdjson/singleheader/simdjson.h`).
   - Validates constraints: Only process logs where the `"status"` field is an integer exactly equal to `200`. Skip any lines missing the `"status"`, `"endpoint"`, or `"latency_ms"` fields.
   - Extracts the `"endpoint"` (string) and `"latency_ms"` (double) features.
   - Aggregates the data to compute the total count, the average `latency_ms`, and the maximum `latency_ms` grouped by `endpoint`.
   - Writes the aggregated summary statistics to `/home/user/summary.csv`. The CSV must have the header `endpoint,count,avg_latency,max_latency` and be sorted alphabetically by endpoint. Output floats with exactly 4 decimal places.
3. Compile your program using the fixed `/app/build.sh`. Your compiled binary must be output to `/home/user/log_analyzer`.

Performance is critical. Your C++ implementation will be evaluated against the Python baseline. To pass, your program's execution time must achieve a speedup of at least 5.0x compared to `/app/baseline.py` while producing functionally identical statistics (averages must be within 0.001 tolerance).