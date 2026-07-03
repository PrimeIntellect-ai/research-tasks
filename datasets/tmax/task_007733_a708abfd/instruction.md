You are assisting a researcher in organizing and processing a messy dataset of environmental sensor readings. 

The raw data is located at `/home/user/raw_sensors.csv`. However, the data collection system had glitches, so many rows are corrupted.

You need to write a Bash script (and/or use standard Unix utilities like `awk`, `sed`, `grep`) to perform a data pipeline that enforces the schema, engineers a new feature using vector math, and selects the most relevant data points. 

Here are your exact requirements:

1. **Schema Enforcement:** 
   Filter the raw data to keep only rows that strictly follow this schema:
   - Exactly 5 columns, comma-separated.
   - Column 1: `Sensor_ID` (alphanumeric string).
   - Columns 2 through 5 (`Temp`, `Pressure`, `Humidity`, `Vibration`): Must be valid numeric values (integers or decimals, optionally prefixed with a `-` sign).
   - Reject any rows with missing fields, extra fields, or non-numeric values in columns 2-5.

2. **Feature Engineering (Linear Algebra):**
   For each valid row, treat the four numeric readings as a vector $X = [Temp, Pressure, Humidity, Vibration]$.
   Compute a new feature called `Risk_Score` by calculating the dot product of $X$ and the predetermined weight vector $W = [0.2, 0.5, -0.1, 1.2]$.
   
3. **Feature Selection:**
   Filter the valid rows to keep only those where the computed `Risk_Score` is strictly greater than `50.0`.

4. **Output Generation:**
   Save the final processed data to `/home/user/high_risk_sensors.csv`.
   - The file must be comma-separated.
   - It should contain 6 columns: `Sensor_ID`, `Temp`, `Pressure`, `Humidity`, `Vibration`, `Risk_Score`.
   - The `Risk_Score` must be formatted to exactly two decimal places (e.g., `59.00`).
   - The rows must be sorted in **descending order** based on the `Risk_Score`.
   - Do not include a header row in the final output file.

Write and execute the necessary commands to generate `/home/user/high_risk_sensors.csv`.