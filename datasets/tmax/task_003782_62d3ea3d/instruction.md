You are managing a configuration tracking system. Raw configuration change logs from various servers are periodically dumped into a single file, but the telemetry stream is noisy and occasionally drops timestamps or malforms entries.

Your task is to write a bash script at `/home/user/process_changes.sh` that processes a log file located at `/home/user/config_changes.log`. 

The script must perform the following tasks:

1. **Validation Checkpoint (Quality Gate)**
   - Scan every line in `/home/user/config_changes.log`.
   - A valid line must strictly match this format: `YYYY-MM-DD HH:MM:SS,SERVICE,ACTION,STATUS`
     - The date/time must be exact (e.g., `2024-05-01 14:32:01`).
     - `SERVICE` must consist only of alphanumeric characters and underscores.
     - `ACTION` must consist only of uppercase letters.
     - `STATUS` must be exactly either `SUCCESS` or `FAIL`.
   - Any line that does not match this format is considered invalid. Write all invalid lines exactly as they appear to `/home/user/invalid_lines.log`.
   - **Quality Gate:** If the total number of invalid lines is strictly greater than 5, the script must print "QUALITY GATE FAILED" to stdout, exit immediately with status code `2`, and skip the remaining steps.

2. **Time-Based Bucketing and Gap-Filling**
   - For all **valid** lines, you need to aggregate the number of `SUCCESS` actions per hour for the specific time window from `2024-05-01 00:00:00` to `2024-05-01 05:59:59` (i.e., hours 00 through 05 inclusive). Ignore logs outside this window or logs with a `FAIL` status.
   - You must output the aggregation to `/home/user/hourly_summary.csv` in the format `YYYY-MM-DD HH:00,COUNT`.
   - **Resampling/Gap-Filling:** Your output must include exactly 6 rows (one for each hour from 00:00 to 05:00). If an hour has no `SUCCESS` configuration changes, it must explicitly output a count of `0` (e.g., `2024-05-01 02:00,0`).

Ensure your script is executable (`chmod +x /home/user/process_changes.sh`). Run your script to generate the required outputs.