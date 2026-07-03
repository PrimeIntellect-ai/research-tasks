You are an operations engineer managing configuration states across a fleet of servers. You need to write a Rust program that processes a heterogeneous configuration change log, extracts the changes, anonymizes sensitive data, and calculates mathematical metrics regarding the frequency of changes.

A log file is located at `/home/user/config_changes.log`. Each line represents a configuration change and has the following format, though the timestamp format varies:
`[{TIMESTAMP}] Server: {IP} | Key: {KEY} | Value: {VALUE}`

The timestamp can be either:
1. An ISO8601 UTC string (e.g., `2023-10-25T14:30:00Z`)
2. A Unix Epoch integer (e.g., `1698244200`)

Your Rust program must perform the following tasks:
1. **Timestamp Alignment & Extraction:** Parse all timestamps and convert them to Unix Epoch seconds (i64).
2. **Data Masking:** Count how many sensitive values were updated per server. A value is considered sensitive and must be masked if its corresponding `{KEY}` contains the substrings `"pass"`, `"secret"`, or `"token"` (case-insensitive). 
3. **Sorting & Grouping:** Group the records by Server IP, and sort the events for each server chronologically by their aligned Unix Epoch timestamp in ascending order.
4. **Mathematical Analysis:** Calculate the *population variance* of the time intervals (in seconds) between consecutive configuration changes for each server. 
   - An interval is the difference in seconds between change $i$ and change $i-1$.
   - The population variance of these intervals is $\frac{\sum (x_i - \mu)^2}{N}$, where $N$ is the number of intervals, $x_i$ is each interval, and $\mu$ is the mean of the intervals.
   - If a server has fewer than 2 intervals (i.e., fewer than 3 configuration changes), its variance should be `0.0`.

Write and execute your Rust program to generate an output JSON file at `/home/user/config_summary.json`.
The output must be a single JSON object where the keys are the Server IPs, and the values are objects with the following exact keys:
- `masked_count` (integer): Total number of sensitive values masked for this server.
- `interval_variance` (float): The population variance of the time intervals, rounded to exactly 2 decimal places.
- `latest_change_epoch` (integer): The Unix Epoch timestamp of the most recent change for this server.

Example Output format:
```json
{
  "10.0.0.1": {
    "masked_count": 2,
    "interval_variance": 25.00,
    "latest_change_epoch": 1698244500
  }
}
```

Ensure your program compiles and runs successfully, and the final JSON is correctly formatted.