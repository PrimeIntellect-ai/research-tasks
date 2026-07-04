You are a data engineer tasked with building a robust ETL script to process a messy application log export.

We have a log export at `/home/user/data/logs.csv` with three columns: `timestamp`, `user_id`, and `log_message`. 
Because of a bug in our legacy system, the `log_message` column contains raw multi-line stack traces and embedded newlines, which often breaks naive line-by-line parsers.

Write a Rust program to process this file. You should create a new Cargo project at `/home/user/etl_project`. You may use popular crates like `csv`, `serde`, `serde_json`, `regex`, and `sha2`.

Your Rust program must perform the following pipeline:
1. **Parse:** Correctly parse the CSV, properly handling the embedded newlines in the `log_message` column.
2. **Extract:** Use regular expressions to extract an error code from the `log_message`. The error code will appear in the format `ErrorCode: E[0-9]+` (e.g., `ErrorCode: E1042`). Extract just the `E[0-9]+` part. If a log doesn't contain an ErrorCode, drop the row.
3. **Deduplicate:** Compute the SHA256 hash of the exact string value of `log_message`. Represent this hash as a lowercase hex string. Deduplicate the logs based on this hash. If multiple logs have the exact same `log_message` hash, keep ONLY the first one encountered in the file.
4. **Sort & Group:** Sort the remaining deduplicated records first by `user_id` (ascending, alphabetically), and then by the extracted `error_code` (ascending, alphabetically).
5. **Output:** Write the final processed records to `/home/user/summary.json`. 

The output must be a JSON array of objects, with the following exact format:
```json
[
  {
    "user_id": "U102",
    "error_code": "E1042",
    "hash": "a1b2c3d4..."
  },
  ...
]
```

Run your Rust program so that the `/home/user/summary.json` file is successfully generated.