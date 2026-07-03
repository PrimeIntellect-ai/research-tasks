You are tasked with building a robust data processing pipeline in Rust to clean and extract changepoints from a messy configuration management log.

A flawed ETL job has been writing configuration states of servers to a log file at `/home/user/raw_configs.txt`. Because of retry mechanisms, the file contains numerous duplicate records. Additionally, some metrics were dropped during ingestion. You need to write a Rust program that orchestrates a pipeline to parse, impute, deduplicate, and extract true changepoints.

**Input Format:**
The file `/home/user/raw_configs.txt` is pipe-delimited (`|`) with the following columns:
`timestamp | server_id | raw_log | cpu_limit`
- `timestamp`: Integer (Unix timestamp).
- `server_id`: String identifier (e.g., `srv-01`).
- `raw_log`: A noisy log string that contains the configuration hash. The hash is always a 6-character alphanumeric string enclosed in brackets, preceded by "hash=" (e.g., `... hash=[a1b2c3] ...`).
- `cpu_limit`: A floating-point number representing the CPU limit metric. Occasionally, this field is empty (whitespace).

**Pipeline Requirements:**
Your Rust program must implement the following logical DAG of operations:

1.  **Feature Extraction (Regex):** Parse the 6-character `config_hash` out of the `raw_log` column for every row.
2.  **Interpolation:** Handle missing `cpu_limit` values by applying linear interpolation grouped by `server_id`. 
    - The data for a server must be sorted by `timestamp` ascending.
    - If a `cpu_limit` is missing at timestamp $t$, find the closest preceding valid value at $t_0$ and the closest succeeding valid value at $t_1$.
    - The interpolated value is: $v(t) = v(t_0) + (v(t_1) - v(t_0)) \times \frac{t - t_0}{t_1 - t_0}$.
    - (Guarantee: The first and last chronologically sorted records for any `server_id` will never have missing `cpu_limit` values.)
3.  **Changepoint Detection (Deduplication):** The ETL job produces duplicates. We only want to keep rows that represent a *true change* in state.
    - Processing chronologically per `server_id`, a row is a "changepoint" if it is the *first* record for that server, OR if its extracted `config_hash` OR its (possibly interpolated) `cpu_limit` differs from the *most recently recorded changepoint* for that server.
    - Floating point comparisons should be exact after rounding to 2 decimal places.

**Output Generation:**
Write the final, cleaned changepoints to a comma-separated file (CSV) at `/home/user/changepoints.csv`.
The CSV must include a header and have the following columns:
`timestamp,server_id,config_hash,cpu_limit`

- `cpu_limit` must be formatted to exactly 2 decimal places (e.g., `10.50`).
- The rows must be sorted by `server_id` (alphabetically ascending), and then by `timestamp` (ascending).

**Constraints:**
- Use Rust (Cargo) to build your solution. You can place your project anywhere, but the final output must be exactly at `/home/user/changepoints.csv`.
- You may use external crates (e.g., `csv`, `regex`, `itertools`).