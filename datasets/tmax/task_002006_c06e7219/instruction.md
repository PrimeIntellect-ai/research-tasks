You are a Data Engineer building an ETL pipeline to process and align time-series data from IoT sensors.

We have two sensors: one for temperature and one for pressure. They log data asynchronously and irregularly.
You will find their raw logs at:
- `/home/user/sensor_temp.csv` (Columns: `timestamp,temp`)
- `/home/user/sensor_press.csv` (Columns: `timestamp,pressure`)

Your task is to write a script in any language you prefer to perform the following operations:
1. **Timestamp Alignment:** Create a regular, strictly 1-minute interval time grid starting exactly at `2023-10-01T10:00:00Z` and ending at `2023-10-01T10:10:00Z` inclusive.
2. **Interpolation & Imputation:**
   - For `temp`, compute the values at the new grid points using **linear interpolation** based on the surrounding raw data points.
   - For `pressure`, compute the values at the new grid points using **forward fill** (i.e., use the value from the most recent prior raw data point).
3. **Constraint-based Validation:** Ensure the aligned output has exactly 11 rows. Furthermore, validate that no values are missing (NaN), that `temp` is always between `10.0` and `50.0`, and that `pressure` is always between `1000.0` and `1100.0`. If any constraint fails, the script should fail (though with the provided data, it should pass).
4. **Output:** Save the final aligned and merged dataset to `/home/user/aligned_sensors.csv`.

**Output File Requirements (`/home/user/aligned_sensors.csv`):**
- Must be a valid CSV file.
- Must have exactly three columns in this order: `timestamp,temp,pressure`.
- `timestamp` must be formatted strictly as ISO8601 strings, e.g., `2023-10-01T10:05:00Z`.
- `temp` and `pressure` should be numerical values (floating point numbers are expected).

Write your script and execute it so that the final output file is generated correctly.