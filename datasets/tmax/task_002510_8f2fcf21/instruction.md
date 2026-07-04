You are an infrastructure data engineer handling data from a configuration manager. A recent ETL job failed and was retried, resulting in a large, messy log file containing duplicate configuration state events. Your task is to clean this data, process it in parallel, and generate an hourly time series of configuration drift.

**Input Data:**
A large JSON Lines file located at `/home/user/raw_config_events.jsonl`.
Each line represents a configuration change event:
`{"timestamp": "2023-10-01T12:34:56Z", "server_id": "srv-12", "config_hash": "a1b2c3d4", "event_id": "evt-98765"}`
Due to the ETL retry, there are exact duplicate rows (same `event_id` and data) that must be ignored. 

**Requirements:**
1. **Large-file streaming:** You must process the file efficiently. Do not load the entire JSONL file into memory at once. Stream it to filter duplicates and partition the events by `server_id`.
2. **Parallel data processing:** You must write a Python script that uses the `multiprocessing` module (e.g., `Pool`) to process the timeline of each `server_id` in parallel.
3. **Resampling and gap-filling:** For each server, reconstruct its configuration state at the *start* of every hour from `2023-10-01T00:00:00Z` to `2023-10-07T23:00:00Z` (inclusive). 
    * A server's state for a given hour is the `config_hash` from its most recent event prior to or exactly at that hour.
    * If a server has no events prior to an hour, it has no state for that hour (it does not contribute).
    * If a server had an event in the past, its state *carries forward* (forward-fill) to subsequent hours until a new event changes it.
4. **Aggregation:** For each hour in the time range, calculate the total number of *unique* `config_hash` values across all currently active servers.
5. **Output:** Write the results to `/home/user/hourly_config_drift.csv`. 
    * The CSV must have exactly two columns: `hour` and `unique_configs`.
    * `hour` should be formatted as an ISO 8601 string (e.g., `2023-10-01T00:00:00Z`).
    * The rows must be sorted chronologically.

Write and execute the Python script to generate the CSV.