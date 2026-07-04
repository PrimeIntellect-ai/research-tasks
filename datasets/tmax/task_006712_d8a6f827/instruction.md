You are a data scientist cleaning up historical IoT weather station data. You have been given a set of CSV files containing sensor readings, but the data is noisy and needs to be aggregated for downstream analysis. 

Your task is to write a Go program at `/home/user/process.go` that reads all CSV files in `/home/user/data/`, processes them concurrently, filters out invalid data, and computes 5-minute windowed averages.

**Requirements:**
1. **Input Data**: The directory `/home/user/data/` contains multiple CSV files. Each CSV has the following header and columns: `timestamp,sensor_id,temperature,humidity`.
   - The `timestamp` is in the format `YYYY/MM/DD HH:MM:SS` (e.g., `2023/10/01 14:23:45`).
2. **Parallel Processing**: Your Go program must process the CSV files concurrently (e.g., using goroutines).
3. **Data Validation**: You must drop any row that violates the following constraints:
   - `-50.0 <= temperature <= 100.0`
   - `0.0 <= humidity <= 100.0`
   - The timestamp must be parsable.
4. **Timestamp Alignment & Aggregation**:
   - Align timestamps to 5-minute tumbling windows. A window starts at the hour and every 5 minutes thereafter (e.g., `10:00:00` to `10:04:59`, `10:05:00` to `10:09:59`).
   - For each window and `sensor_id`, calculate the average `temperature` of the valid rows.
5. **Output**: 
   - Write the aggregated results to `/home/user/summary.jsonl` (JSON Lines format).
   - Each line must be a JSON object with exactly these keys:
     - `"sensor_id"` (string)
     - `"window_start"` (string, formatted as ISO8601 / RFC3339 `YYYY-MM-DDTHH:MM:SSZ`, assuming UTC)
     - `"avg_temperature"` (float, rounded to exactly 2 decimal places)
   - To ensure deterministic output, sort the lines in `/home/user/summary.jsonl` alphabetically before writing them.

Run your script to produce the output file.