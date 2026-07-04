You are acting as a data scientist tasked with cleaning and analyzing a raw dataset of sensor readings.

Your tasks are as follows:
1. You are provided with an SQLite database at `/home/user/raw_data.db`. It contains a single table named `sensor` with columns `timestamp` (TEXT), `temperature` (TEXT), and `pressure` (TEXT).
2. Write and execute a Python script to process this data:
   - Extract all rows from the `sensor` table.
   - Normalize the `temperature` column to Celsius as a float. The raw temperature might end with 'C' for Celsius, 'F' for Fahrenheit, or have no suffix (in which case, assume it is Celsius). The formula for Fahrenheit to Celsius is: `C = (F - 32) * 5/9`.
   - Sort the dataset chronologically by `timestamp` in ascending order.
   - Detect anomalies in the temperature readings. An anomaly is defined as any temperature where the absolute difference between it and the *immediately preceding row's* temperature (in Celsius, after sorting) is strictly greater than `10.0` degrees. The very first row chronologically is never considered an anomaly.
3. Save the processed data:
   - Export the fully cleaned data into a new SQLite database at `/home/user/clean_data.db`, into a table named `clean_sensor`. The table should have the columns: `timestamp` (TEXT), `temperature_c` (REAL), `pressure` (TEXT), and `is_anomaly` (INTEGER, where 1 means true and 0 means false).
   - Export *only* the rows that are flagged as anomalies to a CSV file at `/home/user/anomalies.csv`. The CSV must include a header row with columns: `timestamp`, `temperature_c`, `pressure`.

Ensure your Python script runs successfully and creates the required output files in `/home/user/`.