You are a data analyst tasked with processing a set of messy, fragmented time-series CSV files containing IoT sensor data. The files are located in `/home/user/raw_data/`.

These files contain a mix of valid CSV rows and application log artifacts (like error traces or debug information). 

Your objective is to build a multi-stage data processing pipeline that extracts the valid data, groups it by hour, and calculates the average value for each sensor.

Here are the requirements:
1. **Pipeline Orchestration**: Create a bash script at `/home/user/run_pipeline.sh` that acts as the entry point. It must locate all `.csv` files in `/home/user/raw_data/`.
2. **Regex Filtering**: Inside your bash pipeline, use command-line utilities (e.g., `grep`, `sed`, or `awk`) with regular expressions to filter out the junk log lines. A valid data line *always* starts with a strict ISO 8601-like timestamp (`YYYY-MM-DD HH:MM:SS`), followed by a comma, an alphanumeric sensor ID, a comma, the string `temp`, a comma, and a floating-point number.
3. **Aggregation via Python**: The filtered data must be piped or passed into a Python script you create at `/home/user/aggregate.py`. This script must parse the timestamps, group the data into 1-hour tumbling windows (e.g., `2023-01-01 10:00:00` to `10:59:59` becomes the `2023-01-01 10:00:00` bucket), and calculate the average `temp` for each `sensor_id` in that hour.
4. **Sorting & Output**: The Python script should output a final, clean CSV file to `/home/user/hourly_averages.csv` with the header `timestamp,sensor_id,avg_temp`. The output must be sorted chronologically by the hourly timestamp window, and then alphabetically by `sensor_id`. The `avg_temp` must be rounded to exactly 2 decimal places.

Make sure your `run_pipeline.sh` script is executable and completely automates this process when run.

Example valid input line:
`2023-01-01 10:15:30,S1,temp,22.5`

Example invalid input lines (to be dropped):
`[ERROR] Connection timeout at 10:15`
`2023-01-01 10:15:30,S1,humidity,45.0`
`Header: timestamp,sensor,metric,val`

Expected final output format in `/home/user/hourly_averages.csv`:
```csv
timestamp,sensor_id,avg_temp
2023-01-01 10:00:00,S1,22.60
2023-01-01 10:00:00,S2,23.10
...
```