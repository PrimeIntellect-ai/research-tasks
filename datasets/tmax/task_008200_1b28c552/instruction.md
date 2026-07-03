You are a data analyst working with IoT telemetry data. You have received a batch of sensor logs in a JSON-lines file located at `/home/user/data/telemetry.jsonl`. 

Unfortunately, the system that generated these logs had a bug: some of the JSON lines contain malformed unicode escape sequences in the `msg` field (e.g., `\uXYZ1` instead of valid hex). Standard JSON parsers like `jq` will crash when encountering these lines if not handled properly.

Your task is to write a Bash-based data processing pipeline (you can use standard GNU utilities like `awk`, `sed`, `grep`, `jq`, `sort`, `bc`, etc.) to clean this data, aggregate it, and compute rolling statistics.

Create a script at `/home/user/process.sh` and execute it to produce a final CSV report at `/home/user/rolling_stats.csv`.

Here are the requirements for the processing:

1. **Data Cleaning**: Read `/home/user/data/telemetry.jsonl`. Filter out any lines that are invalid JSON (e.g., due to the broken unicode escapes). You must completely drop the malformed lines. 
   *(Hint: `jq` has ways to handle or skip invalid inputs, or you can use `grep`/`sed` to filter them out before parsing).*

2. **Time-Based Bucketing**: Extract the `device` ID, the `ts` (timestamp), and the `val` (a numeric reading). Truncate the `ts` timestamp to the start of the hour. For example, `2023-10-15T14:35:12Z` becomes `2023-10-15T14:00:00Z`.

3. **Summary Aggregation**: For each `device` and each `hour`, calculate the average of the `val` readings. 

4. **Rolling Statistics**: Sort the aggregated data by `device` (alphabetically) and then by `hour` (chronologically). For each device, compute a 3-hour rolling average of the hourly averages you just calculated. 
   * The rolling window should include the current hour and up to two immediately preceding hours *that are present in the aggregated data*.
   * If only 1 or 2 hours of data exist for a device so far, compute the average over those available hours.

5. **Output Format**: Write the results to `/home/user/rolling_stats.csv` with the following header:
   `device,hour,hourly_avg,rolling_3_avg`
   Round both `hourly_avg` and `rolling_3_avg` to exactly 2 decimal places. 

**Example output structure:**
```csv
device,hour,hourly_avg,rolling_3_avg
DEV01,2023-10-15T13:00:00Z,22.50,22.50
DEV01,2023-10-15T14:00:00Z,24.00,23.25
DEV01,2023-10-15T15:00:00Z,25.50,24.00
DEV01,2023-10-15T16:00:00Z,21.00,23.50
DEV02,2023-10-15T13:00:00Z,10.00,10.00
```

Ensure your `/home/user/process.sh` script has executable permissions and is run to produce the final CSV. You can install tools via `apt-get` if necessary (e.g., `datamash`), but the logic must be driven by your Bash script.