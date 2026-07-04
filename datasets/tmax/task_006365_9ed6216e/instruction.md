You are a data scientist tasked with cleaning and merging two messy IoT sensor datasets. 

You have two files in your home directory:
1. `/home/user/temperature.csv`
2. `/home/user/humidity.csv`

The datasets have the following issues:
- `temperature.csv` is encoded in UTF-16. Its timestamp column `time_str` is formatted as `YYYY/MM/DD HH:MM:SS` (assumed to be UTC). Furthermore, the `sensor_notes` column contains embedded newline characters that cause standard naive line-by-line parsing to fail.
- `humidity.csv` is encoded in UTF-8. Its timestamp column `timestamp` is formatted as an ISO 8601 string `YYYY-MM-DDTHH:MM:SSZ` (UTC).

Your objective is to write and execute a Python script to perform the following data processing pipeline:
1. Load both CSV files correctly, ensuring no rows are dropped due to the embedded newlines in `temperature.csv`.
2. Parse the timestamps in both datasets and convert them into timezone-aware UTC datetime objects.
3. Extract only the `temp_celsius` column from the temperature dataset and the `humidity_percent` column from the humidity dataset.
4. Merge the two datasets based on their timestamps.
5. Create a regular 10-minute frequency time grid starting exactly at `2023-10-01 00:00:00+00:00` and ending at `2023-10-01 02:00:00+00:00` (inclusive).
6. Resample the merged data to this 10-minute grid. Use forward-filling (`ffill`) to fill in any missing values for both temperature and humidity. (The datasets guarantee an initial reading at exactly `2023-10-01 00:00:00+00:00`).
7. Round the forward-filled numeric values to 2 decimal places.
8. Save the resulting aligned and gap-filled dataset to a JSON file at `/home/user/merged_sensors.json`.

The final JSON file must be an array of objects (e.g., Pandas `orient="records"`) with exactly three keys per object:
- `timestamp`: The ISO 8601 string of the 10-minute grid point (e.g., `"2023-10-01T00:10:00Z"`). Note the 'Z' indicating UTC.
- `temp_celsius`: The rounded temperature value.
- `humidity_percent`: The rounded humidity value.

Write the script, run it, and ensure the final JSON file is generated correctly.