You are a data engineer responsible for building an ETL pipeline to process raw server telemetry data. 

There is a raw metrics file located at `/home/user/raw_metrics.csv` containing telemetry data from various servers. The file has a header line and the following columns:
`timestamp,server_id,cpu_usage,memory_bytes`
(where `timestamp` is a Unix epoch integer, `cpu_usage` is a float representing percentage, and `memory_bytes` is an integer).

Your task is to write and execute a Rust program that reads this CSV, performs windowed aggregations, extracts new features, and outputs the processed data to `/home/user/etl_output.jsonl` (a JSON Lines file). 

Requirements for the ETL process:
1. **Time-based Bucketing:** Group the records into tumbling (non-overlapping) 5-minute (300 seconds) windows based on the `timestamp`. A window starts exactly at `window_start = timestamp - (timestamp % 300)`. Groups are identified by `window_start` and `server_id`.
2. **Feature Extraction:** For each record, determine if a "CPU spike" occurred. A CPU spike is defined as `cpu_usage > 90.0`. 
3. **Aggregation & Normalization:** For each bucket and `server_id`, calculate:
   - `avg_cpu`: The arithmetic mean of `cpu_usage` in this window (float).
   - `max_mem_norm`: The maximum `memory_bytes` recorded in this window, normalized to a 0.0 to 1.0 scale relative to an assumed maximum server capacity of exactly 32 GB (`32000000000` bytes). So `max_mem_norm = max_memory_in_bucket / 32000000000.0`.
   - `spike_count`: The total number of CPU spikes that occurred in this window (integer).
4. **Output Format:** Write the aggregated records to `/home/user/etl_output.jsonl`. Each line must be a valid JSON object with the exact keys: `bucket` (integer), `server_id` (string), `avg_cpu` (float), `max_mem_norm` (float), and `spike_count` (integer).
5. **Ordering:** Ensure the output lines are sorted primarily by `bucket` ascending, and secondarily by `server_id` ascending.

You must use Rust to build this pipeline. You may create a Cargo project anywhere in `/home/user/` (e.g., `/home/user/etl_processor`). You can use standard crates like `csv`, `serde`, and `serde_json`. Run your completed pipeline so that the output file is generated correctly.

*Note: The floats should be formatted standardly by `serde_json`, rounding to standard f64 precision is fine.*