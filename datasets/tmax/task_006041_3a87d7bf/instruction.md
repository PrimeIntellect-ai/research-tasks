You are a data analyst troubleshooting an ETL pipeline that handles telemetry from various sensors. The ETL pipeline frequently fails and retries, creating duplicate records and occasionally corrupting data. 

Your task is to write a C program at `/home/user/etl_processor.c` that reads a raw CSV file, cleans the data, resamples it to a fixed interval using linear interpolation, detects anomalies, and outputs a clean CSV file.

### Input Data
The raw data is located at `/home/user/input.csv`. It has the following columns:
`ts,sensor_id,reading`
- `ts`: Integer timestamp (in seconds).
- `sensor_id`: String representing the sensor name.
- `reading`: Floating-point sensor reading.

### Processing Requirements
Your C program must perform the following steps, in order:

1. **Tokenization & Normalization**: Parse the CSV. For the `sensor_id`, strip any leading or trailing whitespace and convert the string to lowercase. You must **only** process rows where the normalized `sensor_id` is `"reactor_temp"`. Ignore all other sensors.
2. **Constraint-based Validation**: Discard any rows where `reading` is less than `0.0` or greater than `5000.0`.
3. **Deduplication**: Because of ETL retries, there may be multiple records with the exact same `ts` for `"reactor_temp"`. If there are duplicates, keep only the record with the **maximum** `reading` value for that timestamp.
4. **Resampling & Gap-Filling**: Resample the cleaned data to a regular **10-second interval**. 
   - The resampled time series must start exactly at the minimum valid timestamp in the cleaned data and end at the maximum valid timestamp.
   - If a target 10-second timestamp exists in the cleaned data, use its exact reading.
   - If a target timestamp does not exist, use **linear interpolation** between the closest valid points before and after the target timestamp. (You can assume the minimum and maximum timestamps will always exist exactly, so you will never need to extrapolate outside the data range).
5. **Anomaly Detection**: In your newly resampled time series, flag any data point as an anomaly if the absolute difference between its reading and the previous resampled point's reading is strictly greater than `100.0`. The first point in the resampled series has no previous point and is never an anomaly.

### Output
The program should generate a file at `/home/user/output.csv` with the following header:
`ts,reading,is_anomaly`

- `ts`: The resampled integer timestamp.
- `reading`: The interpolated/exact reading formatted to exactly one decimal place (e.g., `230.0`).
- `is_anomaly`: `1` if it is an anomaly, `0` otherwise.

Compile your program and run it to produce the `output.csv` file. Ensure the final output is correctly formatted.