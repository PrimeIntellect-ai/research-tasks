You are a data analyst working with a multilingual dataset of IoT sensor logs. The raw data is stored in a CSV file at `/home/user/raw_sensor_logs.csv`. The file is expected to be very large in production, so you must process it using streaming/chunking techniques rather than loading the entire file into memory at once.

Your goal is to write a Python script `/home/user/process_data.py` that processes this CSV and outputs a cleaned, resampled CSV at `/home/user/processed_data.csv`.

Here are the requirements for the processing pipeline:

1. **Filtering & Unicode Handling**: 
   The `sensor_name` column contains sensor names in multiple languages. You must filter the dataset to ONLY include temperature sensors. The valid names for temperature sensors in the dataset are: `TempSensor` (English), `Temperatursensor` (German), and `温度計` (Japanese). Any other sensors (e.g., humidity) must be ignored. In the output, normalize the sensor name to `temperature`.

2. **Information Extraction**:
   The `notes` column contains unstructured text. Embedded within this text is an operational code enclosed in curly braces (e.g., `Device running normally {OK-200} no issues`, or `Failure detected {ERR-502}`). You must extract this code (e.g., `OK-200`, `ERR-502`) and place it in a new column called `op_code`. If no code is found, leave it empty.

3. **Resampling and Gap-Filling**:
   The `timestamp` column contains ISO 8601 timestamps (e.g., `2024-01-01T00:05:23Z`). The readings arrive irregularly. 
   - You must resample the data for the `temperature` sensor to exact 1-minute intervals (e.g., `2024-01-01T00:00:00Z`, `2024-01-01T00:01:00Z`, etc.), starting from the floor of the very first timestamp in the raw dataset to the floor of the last timestamp.
   - If there are multiple readings in a single 1-minute bucket, calculate the mean of the `reading` column for that minute. For the `op_code`, take the last non-empty code seen in that minute.
   - If a 1-minute bucket has no data (a gap), forward-fill the `reading` from the previous minute. Set the `op_code` to `GAP` for these filled rows.

4. **Output Format**:
   The output CSV `/home/user/processed_data.csv` must have exactly these columns, in this order:
   `timestamp` (ISO 8601 format ending in Z), `sensor_name` (always `temperature`), `reading` (rounded to 2 decimal places), `op_code`.

Write and execute the Python script to generate `/home/user/processed_data.csv`. Ensure your script uses the standard `csv` module or pandas with `chunksize` to demonstrate streaming capability.