You are tasked with cleaning up and reconstructing the daily configuration state of our servers using a messy ETL log file. 

Our configuration management system exports server configuration snapshots. Unfortunately, an upstream ETL job has been randomly failing and retrying, resulting in duplicate records on some days and complete gaps on other days.

Your goal is to write a Rust program that parses the unstructured log file, extracts the structured data, handles the duplicates, fills in the missing days, and outputs a clean, sorted CSV file.

**Input:**
A text file located at `/home/user/raw_configs.log` contains unstructured log lines. 
Example line:
`[2023-10-01 14:22:10] INFO - ETL processing config state. target_server=srv-alpha snapshot_hash=a1b2c3d4 retry_count=0`

**Requirements for your Rust program:**
1. **Extraction:** Parse `/home/user/raw_configs.log` to extract the Date (YYYY-MM-DD from the timestamp), the `target_server`, and the `snapshot_hash`. Ignore the time portion and other fields.
2. **Deduplication:** If a server has multiple log entries on the *same day*, keep only the entry with the *latest* timestamp on that day.
3. **Gap-filling (Resampling):** For each unique server, determine its earliest and latest date in the log. For every missing day between a server's earliest and latest date, generate a record using the `snapshot_hash` from the *most recent preceding day*.
4. **Sorting:** The final output must be sorted chronologically by Date (ascending). If multiple servers have an entry for the same date, sort them alphabetically by `target_server` ascending.
5. **Output:** Write the results to `/home/user/clean_configs.csv` with the exact header `date,server,hash`. 

**Environment constraints:**
- Use Rust. You may create a new Cargo project in `/home/user/config_tracker` to write and run your code. 
- You may use popular crates like `chrono`, `regex`, or `csv` if you wish, by adding them to your Cargo.toml.
- Execute your Rust program so that the final `/home/user/clean_configs.csv` is produced.

Once your Rust program finishes writing the CSV, the task is complete.