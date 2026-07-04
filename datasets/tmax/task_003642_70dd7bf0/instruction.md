You are a data engineer tasked with building a robust ETL pipeline in Go to process time-series server metrics.

We have a set of JSON-lines log files located in `/home/user/data/logs/`. Each file contains server telemetry data. However, there's a bug in the upstream logging agent: it occasionally writes malformed unicode escape sequences (e.g., `\uXYZW`) in the `message` field. This causes standard JSON parsers (like Go's `encoding/json`) to fail on those specific lines. 

Your task is to write a Go program (`/home/user/etl.go`) that performs the following steps:
1. **Parallel Processing**: Read all `.jsonl` files in `/home/user/data/logs/` concurrently using goroutines.
2. **Structured Information Extraction**: Extract the `timestamp` (integer, Unix epoch) and `cpu_usage` (float) from each line. Since standard JSON parsing will break on lines with malformed unicode, you must use regex or string manipulation to extract these two fields directly from the raw text.
3. **Hash-based Deduplication**: Multiple log files may contain exact duplicate lines. Compute the SHA-256 hash of each raw string line. If a hash has already been seen globally across any file, discard the line.
4. **Rolling Statistics**: After extraction and deduplication, sort all the parsed records globally by `timestamp` in ascending order. Then, calculate a 3-point rolling average of the `cpu_usage`. The rolling window should include the current point and up to two previous points (if available).
5. **Output**: Write the sorted results to a CSV file at `/home/user/output/metrics.csv` with the headers: `timestamp,cpu_usage,rolling_avg`. Format the `cpu_usage` and `rolling_avg` to exactly 2 decimal places.

Additionally, you need to set up pipeline scheduling:
1. Create a bash script `/home/user/run_etl.sh` that compiles and runs your Go program. Make it executable.
2. Add a cron job for the current user (`user`) that executes `/home/user/run_etl.sh` every 15 minutes.

Constraints:
- Only use standard Go libraries (no third-party packages).
- Create the `/home/user/output/` directory if it does not exist.
- Output floats must be formatted with `%.2f`.