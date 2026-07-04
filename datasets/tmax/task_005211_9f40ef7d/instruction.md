You are tasked with analyzing a sparse configuration change log for a distributed system. The log tracks resource allocations across several microservices. 

You need to write a Go program at `/home/user/process.go` that processes the log file located at `/home/user/config_changes.jsonl` and produces a summary report at `/home/user/summary.json`.

**Input Data Specification:**
The file `/home/user/config_changes.jsonl` contains JSON Lines. Each line has the following fields:
- `timestamp`: The time of the configuration change. This can be either an ISO8601 string (e.g., `"2023-10-01T15:30:00Z"`) or an integer representing UNIX seconds (e.g., `1696174200`).
- `service`: A string representing the service name, which frequently contains Unicode characters and emojis (e.g., `db-東京`, `auth-⚙️`).
- `allocation`: An integer representing the new resource limit configuration.

**Processing Requirements:**
Your Go program must perform the following pipeline:
1. **Validation Gate**: Discard any log entry where the `allocation` is strictly less than `0` or strictly greater than `10000`. These are considered corrupt entries.
2. **Time Alignment**: We are only interested in analyzing the 24-hour period for the date `2023-10-01`, specifically from `2023-10-01T00:00:00Z` to `2023-10-01T23:59:59Z`. For each service, aggregate the valid configuration changes into 24 hourly buckets (Hour 00 to Hour 23). 
   - If multiple valid changes happen in the *same* hour for the same service, use the *latest* chronologically occurring allocation value within that hour.
3. **Imputation (Zero-Order Hold)**: Configuration is stateful. If a service does not have a configuration change recorded in a specific hour bucket, it retains the allocation from the *previous* hour.
   - You must impute all missing hour buckets for the 24-hour period.
   - If a service has no recorded changes prior to a given hour in the day, assume its starting allocation is `0`.
4. **Summary Statistics**: After filling all 24 hourly buckets for each service that appears in the valid logs, calculate:
   - `min`: The minimum allocation across the 24 hourly buckets.
   - `max`: The maximum allocation across the 24 hourly buckets.
   - `avg`: The average allocation across the 24 hourly buckets, rounded to 2 decimal places.

**Output Format:**
Create the result as a pretty-printed JSON file at `/home/user/summary.json`. The keys should be the service names, and the values should be objects containing the statistics.
Example format:
```json
{
  "auth-⚙️": {
    "min": 50,
    "max": 200,
    "avg": 154.17
  },
  "db-東京": {
    "min": 0,
    "max": 600,
    "avg": 550.00
  }
}
```

Run your Go script to produce the summary file. Do not leave the task until `/home/user/summary.json` is correctly generated.