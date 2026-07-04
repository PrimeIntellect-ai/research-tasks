You are a data analyst for a smart city project. We have a batch of messy traffic sensor data in `/home/user/sensor_data.csv`. 

Please write and execute a Python script (e.g., at `/home/user/process_traffic.py`) that processes this data and outputs a cleaned, aggregated file at `/home/user/processed_traffic.csv`. You may install and use `pandas` or any other library you need.

Your data processing script must perform the following steps:
1. **Cleaning:** Remove any rows where `vehicle_count` is less than 0.
2. **Timestamp Alignment:** The `timestamp` column contains mixed formats and timezones. Convert all timestamps to UTC. 
3. **Deduplication:** There are duplicate readings for the same sensor at the same time. Deduplicate based on `sensor_id` and the UTC `timestamp`, keeping only the *first* occurrence.
4. **Parallel Processing:** You must group the data by `sensor_id` and process each group's rolling statistics in parallel using Python's `multiprocessing` or `concurrent.futures` modules.
5. **Rolling Statistics:** For each sensor, compute a 2-hour rolling average of the `vehicle_count`. The 2-hour window for a row at time `T` should include all valid readings for that sensor in the interval `(T - 2 hours, T]` (strictly greater than T minus 2 hours, up to and including T).
6. **Output:** Sort the final combined dataset by `sensor_id` (ascending) and then by `timestamp` (ascending). 

The output file `/home/user/processed_traffic.csv` must be a CSV with the following columns:
- `sensor_id`
- `timestamp` (Formatted strictly as an ISO 8601 string in UTC, e.g., `2023-10-01T10:00:00+00:00` or `2023-10-01 10:00:00+00:00` as pandas outputs by default, but ensure it is timezone-aware and set to UTC).
- `vehicle_count`
- `rolling_avg_2h` (Rounded to 2 decimal places).

Ensure the script runs completely and the output file is generated correctly.