You are helping clean and aggregate a raw dataset of IoT sensor readings.

The input data is located at `/home/user/raw_sensors.csv` and contains comma-separated values with the following header:
`timestamp,sensor_id,temperature,humidity`

The timestamps are in ISO8601 format (e.g., `2023-10-01T12:34:56Z`).

However, the data is noisy. You need to write a Bash script or use command-line tools to process this file and create a cleaned summary at `/home/user/minute_avg_temp.csv`.

Here are the processing requirements:
1. **Validation Checkpoint**: Ignore the header row. Filter out any rows that violate these constraints:
   - `temperature` must be between -50.0 and 150.0 (inclusive).
   - `humidity` must be between 0.0 and 100.0 (inclusive).
   - Rows with empty or non-numeric values for temperature or humidity should be discarded.
2. **Timestamp Alignment**: Align valid timestamps by truncating them to the nearest minute (i.e., set the seconds to `00Z`). For example, `2023-10-01T12:34:56Z` becomes `2023-10-01T12:34:00Z`.
3. **Summary Statistics**: For each aligned minute, calculate the average temperature across all valid sensor readings. 
4. **Output**: Write the results to `/home/user/minute_avg_temp.csv`. 
   - The output must include a header: `timestamp,avg_temperature`
   - The rows must be sorted chronologically by timestamp.
   - The `avg_temperature` must be rounded to exactly one decimal place (e.g., `22.0`, `23.4`).

Please generate the final output file `/home/user/minute_avg_temp.csv` directly. You can use standard Linux utilities (awk, sed, sort, etc.) or write a short script to accomplish this.