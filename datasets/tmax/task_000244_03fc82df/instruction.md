You are tasked with building a configuration management tracking utility in Rust. 
We have a simulated "remote" directory `/home/user/remote_configs/` containing configuration snapshots for multiple servers at different timestamps.

Your goal is to write a Rust program that performs the following pipeline:
1. **Local-Remote Transfer**: "Download" (copy) all `.json` files from `/home/user/remote_configs/` to a local processing directory `/home/user/local_configs/`.
2. **Validation Checkpoint**: Parse each JSON file. Each file has a wide format: 
   `{"server_id": "<string>", "timestamp": <integer>, "metrics": {"max_conn": <float>, "timeout": <float>}}`
   You must validate the data. A configuration is **invalid** if `max_conn <= 0.0` OR if `timeout` is not within the inclusive range `[10.0, 300.0]`. 
   For any invalid files, append their full local filepath (e.g., `/home/user/local_configs/file.json`) to `/home/user/invalid_files.txt` (one per line, sorted alphabetically) and skip them in further processing.
3. **Reshaping and Merging**: For the valid files, flatten (reshape) the wide metrics into a long format and merge them by `server_id` and `timestamp` (ascending order).
4. **Changepoint/Anomaly Detection**: For each `server_id` and each metric (`max_conn`, `timeout`), compare its value at timestamp $T_n$ with its value at the immediately preceding valid timestamp $T_{n-1}$. 
   An **anomaly** is detected if the relative change is strictly greater than 50%. 
   Formula: `|new_value - old_value| / old_value > 0.5`.
5. **Output**: Write all detected anomalies to `/home/user/anomalies.csv` with the exact header `server_id,metric_name,old_value,new_value,timestamp` (where `timestamp` is the timestamp of the *new* value). The rows should be sorted alphabetically by `server_id`, then by `timestamp` (ascending), then by `metric_name`.

**Requirements:**
- Write the application in Rust. You can create the project in `/home/user/config_tracker`.
- You may use standard crates like `serde`, `serde_json`, and `csv`.
- Compile and run your application so that `/home/user/anomalies.csv` and `/home/user/invalid_files.txt` are successfully generated with the correct data.
- Ensure your Rust code handles the calculations using standard 64-bit floats (`f64`). Format the floats in the CSV output to exactly 1 decimal place (e.g., `100.0`).