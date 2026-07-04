I am a researcher organizing climate observation datasets. I have a SQLite database containing raw sensor readings and a separate CSV file containing sensor calibration factors. I need you to write a Python script that joins these data sources, applies the calibrations, aggregates the results, and exports a final JSON report.

Here are the details of the environment and the data:
* Database file: `/home/user/data/observations.db`
  * Table `sensors`: `sensor_id` (INTEGER), `location` (TEXT), `sensor_type` (TEXT)
  * Table `readings`: `reading_id` (INTEGER), `sensor_id` (INTEGER), `timestamp` (DATETIME in 'YYYY-MM-DD HH:MM:SS' format), `raw_value` (FLOAT)
* Calibration file: `/home/user/data/calibration.csv`
  * Columns: `sensor_id` (INTEGER), `correction_factor` (FLOAT)

Write and execute a Python script at `/home/user/process_data.py` that performs the following:
1. Loads data from both `/home/user/data/observations.db` and `/home/user/data/calibration.csv`.
2. Calculates the `corrected_value` for each reading, which is defined as: `raw_value * correction_factor`. (If a sensor is missing from the CSV, assume a `correction_factor` of 1.0).
3. Aggregates the data by the date (ignoring the time part of the timestamp) and `sensor_type`.
4. Calculates the `max_val`, `min_val`, and `avg_val` of the `corrected_value` for each group.
5. Rounds the calculated aggregates (`max_val`, `min_val`, `avg_val`) to exactly 2 decimal places.
6. Exports the result as a JSON file to `/home/user/summary.json`.

The resulting JSON file MUST be an array of objects, sorted first by `date` (ascending) and then by `sensor_type` (ascending). 
Each object must have exactly the following keys:
* `"date"`: String in 'YYYY-MM-DD' format
* `"sensor_type"`: String
* `"max_val"`: Float (rounded to 2 decimal places)
* `"min_val"`: Float (rounded to 2 decimal places)
* `"avg_val"`: Float (rounded to 2 decimal places)

Please create the Python script, run it, and ensure `/home/user/summary.json` is generated exactly as specified.