You are a data engineer tasked with building a robust ETL pipeline to process IoT sensor data. We receive raw, noisy temperature data in a CSV file, and we need to clean, normalize, and resample it using Rust. 

The raw data is located at `/home/user/raw_sensor_data.csv`. 
The CSV has the following columns: `timestamp` (Unix epoch integer), `sensor_id` (string), and `temperature` (float). 

Your task is to write a Rust program that performs the following steps:
1. **Validation & Filtering**: Read the CSV file. A valid temperature must be strictly between -50.0 and 150.0 (inclusive). Any row with a temperature outside this range, or with unparseable/empty values, must be completely discarded.
2. **Normalization & Aggregation**: Group the valid records by `sensor_id` and 1-hour intervals. The 1-hour interval timestamp is calculated as `timestamp - (timestamp % 3600)`. If there are multiple valid readings for a sensor in the same 1-hour interval, compute the arithmetic mean of their temperatures.
3. **Resampling & Gap-Filling**: For each `sensor_id`, identify the minimum and maximum 1-hour interval timestamps present in the *valid* data. For every 1-hour interval between this minimum and maximum (inclusive), there must be a record. If an interval is missing, fill the gap by carrying forward the temperature from the most recent previous valid interval for that sensor (Forward Fill).
4. **Output**: Write the final processed data to a JSON file at `/home/user/processed_data.json`. The JSON should be an array of objects, with each object formatted exactly like this:
   `{"sensor_id":"S1","timestamp":1600000000,"temperature":22.5}`
   The array must be sorted alphabetically by `sensor_id`, and then chronologically by `timestamp` in ascending order. Temperatures should be formatted as standard JSON numbers.

Requirements:
- Create your Rust project in `/home/user/etl_pipeline`.
- You may use external crates like `csv`, `serde`, and `serde_json`.
- Compile and run your program to generate the `/home/user/processed_data.json` file.