You are an operations data scientist working on an IoT platform. A previous data engineer wrote an automated daily report that is supposed to aggregate sensor readings, but the downstream plotting scripts are producing blank dashboards because the data aggregation pipeline outputs empty or malformed files.

Your task is to write a robust Bash script at `/home/user/build_summary.sh` that cleans, joins, and aggregates two raw data files.

The two input files are:
1. `/home/user/data/sensors.tsv`: Contains sensor metadata. Columns: `SensorID`, `Location`, `Status`. (Tab-separated)
2. `/home/user/data/measurements.tsv`: Contains raw sensor readings. Columns: `SensorID`, `Timestamp`, `Value`. (Tab-separated)

Your script `/home/user/build_summary.sh` must perform the following pipeline:
1. **Schema Enforcement:** The `sensors.tsv` file is known to have malformed rows (e.g., missing columns or extra columns due to manual data entry errors). Your script must filter `sensors.tsv` to strictly include only rows that contain exactly 3 columns.
2. **Data Cleaning:** The `measurements.tsv` file is uploaded directly from a legacy Windows server and contains hidden carriage returns (CRLF line endings). If not handled properly, these characters cause standard Unix tools (like `join` or `awk`) to fail silently or produce corrupted output. Your script must clean these line endings.
3. **Multi-source Joining:** Join the cleaned, schema-compliant sensors data with the measurements data on the `SensorID` field.
4. **Transformation & Aggregation:** 
   - Filter the joined data to keep only rows where the sensor `Status` is exactly `ACTIVE`.
   - Calculate the maximum `Value` recorded for each `Location`.
5. **Output:** The script must write the final aggregated results to `/home/user/max_values.tsv`.
   - The file must be tab-separated.
   - It must include a header row: `Location\tMaxValue`.
   - The rows must be sorted alphabetically by `Location`.
   - The script should execute successfully without user input and produce the correct output file.

You may use any standard Unix utilities (`awk`, `sed`, `sort`, `join`, `tr`, etc.). When you are done, run your script to generate the `/home/user/max_values.tsv` file so it can be verified.