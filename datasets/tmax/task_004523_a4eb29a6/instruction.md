You are a data engineer troubleshooting an ETL pipeline. A scheduled job failed midway and was blindly retried, resulting in an output log file containing duplicate records. The log file also has missing data for certain periods due to a brief upstream outage. 

Your task is to build a Bash-only script that processes this messy log file, reconstructs the timeline, and calculates specific rolling statistics.

**Task Requirements:**

1. **Local-Remote Transfer**: A raw log file has been dropped into a staging directory at `/var/tmp/etl_drop/server_metrics.log`. Copy this file to `/home/user/workspace/raw.log` before processing it.
2. **Deduplication**: The file contains exact duplicate lines because of the ETL retry. You must filter out these exact duplicates before performing any aggregations.
3. **Structured Information Extraction**: The log lines look like this:
   `[2023-10-14 10:01:45] INFO [MetricAgent] CPU_USAGE=47.1% Memory=1030MB`
   Extract the minute-level timestamp (e.g., `2023-10-14 10:01`) and the numeric `CPU_USAGE` value (e.g., `47.1`).
4. **Time-based Bucketing**: Calculate the average CPU usage for each minute. If a minute has multiple distinct entries, average their CPU values.
5. **Resampling and Gap-Filling**: You must ensure there is a continuous minute-by-minute timeline strictly from `2023-10-14 10:00` to `2023-10-14 10:10` (inclusive, 11 total minutes). If a minute has no data in the log, forward-fill the average CPU value from the most recent available minute. (Assume `10:00` always has data).
6. **Rolling Statistics**: Calculate a 3-minute rolling average of the minute-level aggregated CPU usage. For a given minute, this is the average of the CPU value for that minute and the previous two minutes. If fewer than 3 minutes are available (e.g., at `10:00` or `10:01`), average the available minutes.
7. **Output Format**: Write your final results to `/home/user/workspace/etl_output.csv` with exactly the following format:
   - A header row: `Timestamp,Avg_CPU,Rolling_Avg_CPU`
   - Data rows: `YYYY-MM-DD HH:MM,XX.X,YY.Y`
   - All numeric values must be rounded to exactly 1 decimal place.

**Rules:**
- You must use standard Bash built-ins, coreutils, and standard CLI tools (e.g., `awk`, `sed`, `grep`, `sort`, `uniq`, `bash`). Do not use Python, Perl, Ruby, or other programming languages.
- Create `/home/user/workspace/` if it does not exist.
- Ensure the final output file `/home/user/workspace/etl_output.csv` exactly matches the required CSV format.