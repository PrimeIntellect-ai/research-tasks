You are a data engineer building an ETL pipeline to process raw telemetry logs from a fleet of mobile sensors. The sensors periodically send their (x, y) coordinates, but the log format is messy, sometimes missing data, and mixed with testing logs. 

Your objective is to extract the data, clean it, interpolate missing values, and calculate the total distance traveled by each valid sensor.

Here is what you need to do:
1. **Read the raw logs** from `/home/user/sensor_stream.log`. The file contains messy log lines. You must use Regular Expressions to extract:
   - The timestamp (ISO 8601 format, enclosed in brackets at the start of the line).
   - The `sensor_id` (prefixed by `sensor_id: `).
   - The JSON payload containing `x` and `y` coordinates (prefixed by `payload: `).
2. **Validate and filter** the records: 
   - Only process records where the `sensor_id` strictly matches the format `SN-` followed by exactly 4 digits (e.g., `SN-1234`). Ignore all other sensors (e.g., `TEST-01`, `SN-99`).
3. **Impute missing data**:
   - Some payloads are missing the `x` value, missing the `y` value, or have them set to `null`.
   - For each valid sensor, sort its records chronologically by timestamp.
   - Use time-based linear interpolation to fill in any missing `x` or `y` coordinates. You can assume that the chronologically first and last records for any valid sensor will always have both `x` and `y` present.
4. **Compute total distance**:
   - For each valid sensor, calculate the total Euclidean distance traveled across its chronological path (including the interpolated points).
5. **Output the results**:
   - Write a JSON file to `/home/user/distances.json`.
   - The keys should be the valid `sensor_id` strings, and the values should be their total distance traveled as a float, rounded to exactly 2 decimal places.
   
Example output format (`/home/user/distances.json`):
```json
{
  "SN-1001": 15.34,
  "SN-2005": 0.00
}
```

Write a Python script to perform this pipeline and execute it.