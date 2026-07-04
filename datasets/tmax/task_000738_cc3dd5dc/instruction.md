You are a Database Reliability Engineer (DBRE) tasked with analyzing an enormous volume of NoSQL backup metadata. We need to identify backups that took unusually long to complete, which could indicate disk degradation or anomalous data bloat.

We have an existing Rust-based log analysis tool located at `/app/backup-analyzer`. It reads a large JSONLines file of backup metadata (`/home/user/backup_logs.jsonl`), calculates a 7-backup rolling average of the `duration_seconds` per `cluster_id`, and flags backups whose duration exceeds 2.5x their rolling average. It then exports these anomalies to `/home/user/anomalies.csv`.

However, the current implementation is broken and extremely slow:
1. The tool currently fails to build due to a misconfigured dependency in its `Cargo.toml`.
2. The anomaly detection logic in `src/main.rs` uses a naive O(N^2) nested loop over the data, which is completely unscalable for our production dataset (over 500,000 records).

Your tasks:
1. **Fix the package configuration:** Inspect `/app/backup-analyzer/Cargo.toml` and resolve the compilation issue (hint: a critical feature flag required for the Polars dataframe library is missing).
2. **Optimize the querying and aggregation:** Rewrite the analytical aggregation logic in `src/main.rs` to use O(N) operations, such as Polars' built-in window functions (e.g., `rolling_mean`) or an efficient single-pass iterator grouped by `cluster_id`.
3. **Format and Export:** Ensure the tool still filters the data correctly (duration > 2.5 * rolling average) and exports the results to `/home/user/anomalies.csv`. The output CSV must include the columns `cluster_id`, `timestamp`, `duration_seconds`, and `rolling_avg`, sorted by `timestamp` descending.
4. **Meet the Performance Threshold:** Your rewritten Rust binary (compiled in release mode) must execute in under **1.5 seconds** on the provided dataset.

The dataset is located at `/home/user/backup_logs.jsonl` and has the following schema:
`{"cluster_id": "string", "timestamp": "ISO8601 string", "size_bytes": integer, "duration_seconds": float, "status": "string"}`

To complete the task, modify the code, build the optimized release binary (`cargo build --release`), and run it to produce the `anomalies.csv`. Verification will test both the correctness of your CSV and the execution time of your compiled binary.