You are a data analyst troubleshooting thermal issues in a server rack. You have two data sources: unstructured text logs from a temperature sensor, and a structured CSV containing server CPU load metrics. They are collected in different formats and timebases.

Your task is to extract, align, and aggregate these two datasets into 10-minute intervals to find the correlation between server load and temperature.

**Data Sources:**
1. `/home/user/sensor_logs.txt`: Unstructured log file containing temperature readings mixed with other system logs.
   - Example line: `[INFO] [12-Oct-2023 12:02:30 UTC] Thermal probe reported temp: 40.5C in Zone 1`
   - Some lines do not contain temperature readings and should be ignored.
   - The timestamp is enclosed in brackets and uses the format `DD-MMM-YYYY HH:MM:SS UTC`.

2. `/home/user/server_load.csv`: A CSV file containing CPU load percentages.
   - Format: `timestamp,load_percentage`
   - Example line: `1697112100,50.0`
   - The timestamp is an integer UNIX epoch timestamp.

**Processing Requirements:**
1. Parse the timestamps from both files.
2. Align the data into 10-minute buckets. A bucket starts at the top of the hour, 10 minutes past, 20 minutes past, etc. (e.g., a reading at `12:02:30` falls into the `12:00:00` bucket, which is represented by the UNIX epoch for `12:00:00`).
3. For each 10-minute bucket, calculate:
   - The average temperature (extracted from the log text).
   - The average CPU load.
4. Perform an INNER JOIN on the aggregated buckets (only include 10-minute buckets that have BOTH temperature readings and CPU load data).

**Output:**
Create a CSV file at `/home/user/aligned_summary.csv` with the following requirements:
- Headers: `interval_start_epoch,avg_temp,avg_load`
- Rows must be sorted chronologically by `interval_start_epoch` in ascending order.
- `avg_temp` and `avg_load` must be rounded to exactly 2 decimal places.