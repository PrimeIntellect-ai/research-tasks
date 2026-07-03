You are a data engineer tasked with building a lightweight ETL pipeline in Rust. We have two data sources containing recent server logs and user metadata. 

Your objective is to write and execute a Rust program that processes these files, joins them, extracts specific text features, gap-fills missing time periods, and logs its execution.

### Environment & Setup
- Create your Rust project in `/home/user/etl_project`.
- The input files are located at:
  1. `/home/user/data/server_logs.txt`: A plain text file where each line follows the format:
     `[YYYY-MM-DD HH:MM] <USER_ID> <ACTION> <PAYLOAD>`
     Example: `[2024-03-15 08:14] U105 CONNECT IP:192.168.1.1`
  2. `/home/user/data/users.csv`: A CSV file with headers `user_id,tier`.
     Example: `U105,premium`

### Pipeline Requirements
1. **Join & Merge**: Combine the log events with the user tiers using the `USER_ID`. Ignore any logs where the `USER_ID` does not exist in `users.csv`.
2. **Feature Extraction**: Extract the "resource_type" from the `<PAYLOAD>` string. The `resource_type` is defined as the text *before* the first colon (`:`) in the payload. If there is no colon, the `resource_type` is the entire payload string. (e.g., `IP:192.168.1.1` -> `IP`, `TIMEOUT` -> `TIMEOUT`).
3. **Resampling & Gap-filling**: 
   - We want to aggregate the count of actions per hour, per tier, per resource_type.
   - Truncate the timestamps to the hour (e.g., `[2024-03-15 08:14]` becomes `2024-03-15 08:00`).
   - **Crucial**: For the timeframe starting exactly at `2024-03-15 08:00` and ending at `2024-03-15 10:00` (inclusive of 08:00, 09:00, and 10:00), you must ensure that for *every* hour in that range, and for *every* known `tier` present in `users.csv`, there is a record in the output for the resource_type `"IP"`. If no such events occurred, fill the gap with a count of `0`. (You do not need to gap-fill for other resource types).
4. **Output**: Write the aggregated results to `/home/user/output/summary.csv` with the exact headers: `hour,tier,resource_type,count`. Sort the output ascendingly by `hour`, then `tier`, then `resource_type`.
5. **Pipeline Logging**: Upon successful completion, your Rust program must append the following exact line to `/home/user/pipeline.log`:
   `ETL SUCCESS: Processed <N> valid log entries` (where `<N>` is the number of log lines that successfully joined with `users.csv`).

Write the Rust code, compile it, and run it to produce the output files. Create any necessary output directories. You may use external crates like `chrono`, `csv`, or `serde` if you configure them in your `Cargo.toml`.