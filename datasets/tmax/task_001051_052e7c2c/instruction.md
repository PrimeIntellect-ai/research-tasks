You are tasked with replacing a legacy, undocumented data processing component for our log analytics pipeline. 

We have an old, stripped binary located at `/app/legacy_aggregator` that processes our proprietary binary log format. The pipeline suffers from an issue where upstream ETL jobs produce duplicate records when retried. The legacy binary handles these duplicates, resamples the data, and performs windowed aggregations. It's currently a black box, and it runs too slowly. We need a parallelized C implementation to replace it.

**The Mission:**
Write a C program that exactly replicates the behavior of `/app/legacy_aggregator`. Compile your solution to `/home/user/log_cleaner`. We will fuzz your program against the legacy binary with millions of records to ensure bit-exact equivalence.

**Binary Input Format (Standard Input):**
A continuous stream of 24-byte structs:
- `uint64_t timestamp` (Unix epoch seconds)
- `uint32_t metric_id`
- `uint32_t is_retry` (1 if this is a retry record, 0 otherwise)
- `double value`

**Binary Output Format (Standard Output):**
A continuous stream of 20-byte structs:
- `uint64_t window_end_ts`
- `uint32_t metric_id`
- `double rolling_sum`

**High-Level Pipeline Expectations (to guide your reverse engineering):**
1. **Deduplication:** When multiple records for the same `metric_id` arrive at the exact same `timestamp`, the record with the highest `is_retry` flag takes precedence. If `is_retry` flags are identical, the last received record wins.
2. **Resampling & Gap Filling:** The logs often skip seconds. The system resamples the timeline to 1-second intervals. Missing values are filled using a forward-fill mechanism (carrying over the last known value for that `metric_id`).
3. **Windowed Aggregation:** Computes a 5-second rolling sum for each `metric_id` (current second + 4 previous seconds).
4. **Parallelization:** Your implementation should handle multiple `metric_id` streams concurrently (e.g., using pthreads) for performance.

**Constraints:**
- Your program must read from `stdin` and write to `stdout`.
- Input streams are guaranteed to be sorted by timestamp per `metric_id`, but different metrics might be interleaved.
- Compile your code with: `gcc -O3 -pthread /home/user/solution.c -o /home/user/log_cleaner`

Investigate the binary, infer the exact edge-case logic (e.g., initial state of missing values before the first record, boundary conditions of the rolling sum), and provide your bit-exact C replacement.