You are a data engineer tasked with building an ETL (Extract, Transform, Load) pipeline. 

We have two raw data sources in `/home/user/data/`:
1. `/home/user/data/sensors.csv`: Contains metadata about deployed sensors.
   Columns: `sensor_id` (integer), `location` (string), `is_active` (boolean: true/false).
2. `/home/user/data/readings.json`: Contains a stream of sensor readings. It is a JSON array of objects.
   Keys: `reading_id` (string), `sensor_id` (integer, string, or null), `value` (float).

Write a script in the language of your choice to process this data. Your pipeline must:
1. Load both datasets.
2. Filter the readings to keep only those that have a valid, non-null `sensor_id`.
3. Join the valid readings with the sensor metadata.
4. Filter the results to include ONLY readings from sensors where `is_active` is `true`.
5. Ensure the `sensor_id` does not get silently corrupted into a float (e.g., `101.0`) due to missing values in the pipeline. It must remain a clean integer representation.
6. Write the cleaned and merged dataset to `/home/user/output/clean_readings.csv`. The output CSV must have exactly these columns in this order: `reading_id,sensor_id,location,value`. There should be no float representations of the `sensor_id`.
7. Write a summary report to `/home/user/output/report.txt` with exactly the following two lines:
   Total valid readings: <count>
   Sum of values: <sum>
   (Replace `<count>` with the integer count of rows in the output CSV, and `<sum>` with the sum of the `value` column rounded to 1 decimal place).

Constraints:
- Create the `/home/user/output/` directory if it does not exist.
- Treat string representations of integers in the JSON `sensor_id` (e.g., `"101"`) as valid IDs equivalent to their integer counterparts.