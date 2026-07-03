You are an automation specialist managing an IoT sensor network. Your team receives regular data dumps in a "wide" CSV format, where each row represents a single timestamp and columns represent different sensors. 

Your task is to create an automated workflow using Python to reshape, aggregate, and report on this time-series data.

**Inputs:**
1. `/home/user/wide_sensors.csv`: A CSV file containing time-series data. The first column is `timestamp`, and the remaining columns are sensor names (e.g., `sensor_alpha`, `sensor_beta`). Some values may be empty (missing).
2. `/home/user/template.md`: A markdown template file for generating reports.

**Requirements:**
Write a Python script at `/home/user/process_sensors.py` and run it to perform the following operations:
1. **Reshape:** Read `/home/user/wide_sensors.csv` and convert it from a wide format to a long format with columns: `timestamp`, `sensor_name`, and `value`. Drop any rows where the `value` is missing or empty.
2. **Sort & Group:** Sort the long-format data primarily by `sensor_name` (alphabetically) and secondarily by `timestamp` (chronologically, oldest to newest).
3. **Calculate:** For each sensor, calculate:
   - Maximum value
   - Minimum value
   - Average value (strictly rounded to exactly 2 decimal places, e.g., `14.50`)
4. **Generate Reports:** Read `/home/user/template.md`. For each sensor, create a new report file at `/home/user/reports/<sensor_name>.md`. 
   Replace the following exact placeholders in the template:
   - `{SENSOR}` -> The sensor's name
   - `{MAX}` -> The maximum value (formatted to 1 decimal place)
   - `{MIN}` -> The minimum value (formatted to 1 decimal place)
   - `{AVG}` -> The average value (formatted to 2 decimal places)
   - `{TABLE}` -> A markdown table of the **last 3** (most recent) readings for this sensor. The table must have exactly this format:
     ```markdown
     | Timestamp | Value |
     |---|---|
     | 2023-10-01T10:10:00 | 15.2 |
     | 2023-10-01T10:15:00 | 14.8 |
     | 2023-10-01T10:20:00 | 15.5 |
     ```
     *(If a sensor has fewer than 3 readings, include all available readings sorted oldest to newest).*

**System State Requirements:**
- Create the output directory `/home/user/reports/` if it does not exist.
- Ensure your Python script executes successfully and creates the required markdown files. Do not use external libraries other than `pandas` (which is pre-installed) and standard Python libraries.