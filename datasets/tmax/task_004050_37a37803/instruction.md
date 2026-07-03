You are tasked with building a strict CSV processing pipeline in C that aggregates sensor data while robustly handling missing values and outliers.

A common pitfall in data analysis (similar to pandas silently converting integer arrays to floats when NaNs are introduced) is C's tendency to parse empty numeric strings as `0` when using naive functions like `atoi()` or `sscanf()`. Your solution must avoid this.

Data description:
You will process a file located at `/home/user/sensors.csv` (which is already present on the system).
The CSV has a header row and four columns:
`timestamp,sensor_id,temperature,error_code`
- `timestamp`: string (ISO 8601, ignore for processing)
- `sensor_id`: integer
- `temperature`: float
- `error_code`: integer (CAN BE MISSING, i.e., empty string)

Requirements for your C program (`/home/user/process_sensors.c`):
1. **Schema & Missing Value Handling:** Parse the CSV carefully. If the `error_code` field is completely empty (e.g., ends in `,` before the newline), you must treat it as having the value `-1`. Do NOT let it default to `0`.
2. **Outlier Rejection:** Discard any row where the `temperature` is an outlier. An outlier is defined as `temperature < -50.0` or `temperature > 150.0`.
3. **Filtering:** Only aggregate rows that have a valid reading. A reading is valid if its `error_code` is either `0` (no error) or `-1` (missing error code). Discard rows with any other error code (e.g., 1, 2, 404).
4. **Aggregation:** Calculate the average temperature for each `sensor_id` using only the valid, non-outlier rows.
5. **Output Validation & Export:** Write the aggregated results to `/home/user/summary.csv`. The output must contain a header `sensor_id,avg_temperature`. The rows must be sorted by `sensor_id` in ascending order. The `avg_temperature` must be formatted to exactly two decimal places (e.g., `23.50`).

Compile your program as `/home/user/process_sensors` using standard `gcc` (you may use `-O2` and `-lm` if needed), and run it to produce the `summary.csv` file.