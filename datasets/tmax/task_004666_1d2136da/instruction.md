You are a data engineer tasked with building a robust ETL pipeline for an IoT sensor network in a smart factory. You need to process a time-series dataset of temperature and humidity readings, handling missing values, filtering outliers, and aggregating the data. 

You must write a C++17 program (using only the Standard Template Library) to perform this pipeline.

**Input Data:**
You will be provided with a raw CSV file at `/home/user/raw_sensors.csv`.
The file has a header and the following format: `timestamp_ms,sensor_id,temperature,humidity`
- `timestamp_ms`: A 64-bit integer representing epoch time in milliseconds.
- `sensor_id`: A string representing the sensor (e.g., "A", "B").
- `temperature`: A floating-point number. Some entries will be empty strings (meaning missing data).
- `humidity`: A floating-point number. Some entries will be empty strings (meaning missing data).

**Processing Pipeline Requirements:**

1. **Validation Checkpoints (Filtering):**
   - As you parse the data, check the `temperature` value (if present). If the temperature is strictly greater than `100.0` or strictly less than `-50.0`, the entire row is considered an anomaly and must be completely dropped.
   - For every dropped row, you must log a warning to `/home/user/pipeline.log` in this exact format:
     `[WARN] Dropped row with timestamp <timestamp_ms> due to out-of-bounds temperature.`
   - Do this *before* performing any interpolation.

2. **Interpolation (Imputation):**
   - After filtering, you must fill in any missing `temperature` or `humidity` values using **linear interpolation** based on time.
   - Interpolation must be done *per sensor_id*.
   - Formula: `v = v1 + (v2 - v1) * (t - t1) / (t2 - t1)`, where `t1` is the timestamp of the last available value before the missing one, and `t2` is the timestamp of the next available value.
   - You can assume that the very first and very last row for each sensor will never have missing values, and missing values will not occur consecutively for the same sensor/metric.

3. **Time-based Bucketing and Aggregation:**
   - Group the cleaned/interpolated data into 15-minute buckets (15 minutes = 900,000 milliseconds).
   - The bucket boundary is determined by `timestamp_ms / 900000 * 900000` (integer division).
   - For each bucket and each `sensor_id`, calculate the average (mean) `temperature` and average `humidity`.

4. **Output Generation:**
   - Write the aggregated data to a CSV file at `/home/user/aggregated_sensors.csv`.
   - The output must include a header: `bucket_start_ts,sensor_id,avg_temp,avg_humidity`
   - The `avg_temp` and `avg_humidity` must be formatted to exactly 2 decimal places.
   - Sort the output CSV chronologically by `bucket_start_ts` ascending. If multiple sensors have the same bucket start time, sort them alphabetically by `sensor_id`.
   - Once all processing is complete, append a final log message to `/home/user/pipeline.log`:
     `[INFO] Pipeline finished.`

**Task Instructions:**
1. Write the C++ code to a file named `/home/user/process_sensors.cpp`.
2. Compile it using `g++ -std=c++17 /home/user/process_sensors.cpp -o /home/user/process_sensors`.
3. Execute the binary to generate `/home/user/aggregated_sensors.csv` and `/home/user/pipeline.log`.