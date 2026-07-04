You are acting as a log analyst investigating a sudden surge in anomalous traffic. You have been given a raw, unordered, and noisy log file. Your task is to build a robust data processing pipeline in Rust to clean, deduplicate, group, and analyze these logs.

**Input Data:**
The raw log file is located at `/home/user/data/raw_logs.txt`.
Each line is pipe-separated (`|`) and follows this exact format:
`Timestamp|IP_Address|User_Agent|Status_Code|Endpoint`
- `Timestamp`: Integer (Unix Epoch)
- `IP_Address`: String (IPv4)
- `User_Agent`: String
- `Status_Code`: Integer
- `Endpoint`: String

**Pipeline Requirements:**

1. **Project Setup:**
   Create a new Rust project in `/home/user/log_processor`. You may use standard crates like `serde`, `serde_json`, and `fnv` or `ahash` if you wish, but the choice is yours.

2. **Hash-Based Deduplication:**
   The log file contains exact duplicates due to a bug in the logging router. You must deduplicate the log entries. Two log entries are considered identical duplicates if their `(Timestamp, IP_Address, Endpoint)` tuple is exactly the same. You must keep only the *first* occurrence of any such duplicate found in the file, discarding the rest. 

3. **Sorting and Grouping:**
   After deduplication, group the remaining logs by `IP_Address`. 
   Within each IP group, sort the log entries chronologically by `Timestamp` in ascending order.

4. **Pipeline Output:**
   Write the grouped and sorted logs to `/home/user/processed_logs.jsonl` in JSON Lines format. 
   The lines in this file must be sorted alphabetically by `IP_Address`.
   Each line must be a JSON object with the following schema:
   ```json
   {
     "ip": "192.168.1.10",
     "logs": [
       {
         "timestamp": 1690000000,
         "user_agent": "Mozilla/5.0",
         "status_code": 200,
         "endpoint": "/api/v1/login"
       }
     ]
   }
   ```

5. **Pipeline Logging and Monitoring (Metrics):**
   To ensure the pipeline is working as expected, your Rust application must output a final monitoring metrics file to `/home/user/metrics.json` containing the following exact JSON schema:
   ```json
   {
     "total_raw_lines": 0,
     "total_deduplicated_lines": 0,
     "unique_ips": 0
   }
   ```
   - `total_raw_lines`: The number of lines read from the input file.
   - `total_deduplicated_lines`: The number of log entries remaining *after* the deduplication step.
   - `unique_ips`: The number of unique IP addresses (groups) found in the deduplicated data.

Build and run your Rust project to produce the two output files: `/home/user/processed_logs.jsonl` and `/home/user/metrics.json`.