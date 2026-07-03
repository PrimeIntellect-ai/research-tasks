You are tasked with auditing a fleet's configuration changes. You have been provided with a CSV file at `/home/user/config_history.csv` which contains historical configuration updates for several servers. The data is currently in a wide format.

Your goal is to write a Python script that processes this file to extract and analyze the memory configuration changes.

Please perform the following steps:
1. **Reshape the Data**: Convert the wide-format CSV into a long format where each row represents a single configuration parameter update. The original columns are `time`, `server`, `cpu_cores`, `memory_max`, and `disk_gb`. Blank or empty values mean the parameter was not updated during that event and should be dropped.
2. **Validate Constraints**: Filter out any rows containing invalid configuration values. The valid mathematical bounds (inclusive) for the parameters are:
   - `cpu_cores`: 1 to 128
   - `memory_max`: 256 to 32768
   - `disk_gb`: 10 to 10000
   Any updates falling outside these ranges are considered corrupted and must be completely discarded from the analysis.
3. **Sort and Group**: Focus only on the `memory_max` parameter after validation. Sort the valid `memory_max` updates by `server` (alphabetically) and then by `time` (chronologically).
4. **Rolling Aggregation**: For each server's `memory_max` history, calculate a 3-event rolling average. This means the average of the current valid `memory_max` value and up to two immediately preceding valid `memory_max` values for that specific server.
5. **Output**: Save your results to `/home/user/memory_audit.csv`. The output must be a CSV file with exactly the following columns, in order: `server`, `time`, `memory_max`, `rolling_avg_3`.
   - The `rolling_avg_3` values must be rounded to exactly 2 decimal places (e.g., `1024.00`, `2389.33`).
   - The file must remain sorted by `server` (ascending) and `time` (ascending).

Write and execute the Python code necessary to produce `/home/user/memory_audit.csv`.