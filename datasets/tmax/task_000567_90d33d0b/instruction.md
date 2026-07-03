You are acting as a Database Administrator and Rust developer. We have an SQLite database located at `/home/user/metrics.db` that logs device telemetry. 

Recently, the database suffered a partial corruption issue affecting the `idx_measurements_ts` index, causing it to occasionally return stale or out-of-order rows. 

Your task is to write a Rust utility that safely queries this data, computes an analytical aggregation, and outputs a paginated report. 

We have already set up a Cargo project for you at `/home/user/metrics_processor` with the `rusqlite` crate included.

Here are your requirements:
1. Reverse engineer the schema of `/home/user/metrics.db` to understand the relationships between devices and their measurements.
2. In your Rust program (`/home/user/metrics_processor/src/main.rs`), you must first execute the SQL command `REINDEX idx_measurements_ts;` to fix the index before querying.
3. Your program must accept a single command-line argument: a float `threshold`.
4. Construct a parameterized query using a Window Function to calculate a `rolling_avg`: the average of the `reading` column for the current row and the **strictly previous 2 rows** for the same device, ordered by `timestamp`.
5. Join the tables to get the device's name.
6. Filter the results such that you only return rows where the ORIGINAL `reading` is strictly greater than the `threshold` parameter (use a parameterized query for this threshold, do not inject it as a string).
7. Sort the final filtered results by device name (ASC), then by timestamp (ASC).
8. Paginate the result: return exactly 10 rows, skipping the first 5 rows (i.e., LIMIT 10 OFFSET 5).
9. The Rust program should execute the query and write the results to `/home/user/results.csv`. The CSV must have the following header: `device_name,timestamp,reading,rolling_avg`. Format the `rolling_avg` to exactly 2 decimal places.

To complete the task, build and run your Rust program with a threshold of `45.0`:
`cd /home/user/metrics_processor && cargo run -- 45.0`

Ensure the final output file `/home/user/results.csv` is correctly generated.