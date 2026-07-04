You are a log analyst investigating a pattern of internationalized error messages and their correlation with system load. You have two datasets that were collected from different remote servers:

1. `/home/user/app_logs.csv`: Contains application logs with Epoch timestamps, UserIDs, and multi-language messages.
   Format: `Timestamp,UserID,Message`
2. `/home/user/sys_metrics.csv`: Contains system metrics with ISO8601 timestamps (UTC), CPU Load, and Memory Load.
   Format: `Timestamp,CPU_Load,Mem_Load`

Your task is to write and execute a Bash script (e.g., using `awk`, `sed`, `date`, `join`, or purely bash) that performs the following:

1. **Time-based bucketing and Timestamp alignment:** Parse the timestamps from both files and align them into 1-hour buckets (e.g., any time from `12:00:00` to `12:59:59` belongs to the `12:00:00` bucket). Assume all times are in UTC.
2. **Unicode text processing:** Identify application logs that contain either the Chinese characters "故障" (meaning Fault) OR the Russian word "Сбой" (meaning Failure).
3. **Joins and Aggregation:** Join the two datasets based on their 1-hour time buckets. For each 1-hour bucket that has **at least one** matching fault/failure message, calculate the **maximum** `CPU_Load` during that hour, and count the total number of fault/failure messages in that hour.
4. **Output:** Generate a tab-separated file at `/home/user/report.tsv` containing the aggregated results sorted chronologically.

The output format of `/home/user/report.tsv` must be strictly:
`YYYY-MM-DD HH:00:00\t<Max_CPU_Load>\t<Count_of_faults>`

Note: 
- Use standard floating point comparison for maximum CPU load.
- Ensure your script correctly converts and truncates the Epoch and ISO8601 timestamps to the start of the hour in `YYYY-MM-DD HH:00:00` format.
- Output floats exactly as they appear in the source or with standard precision if computed, but since you are finding the maximum, you can print the exact string from the CSV.