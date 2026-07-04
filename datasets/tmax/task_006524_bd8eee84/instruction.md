You are a data engineer tasked with building a high-performance ETL pipeline in C to process IoT temperature sensor data. We receive massive, continuous streams of data, so your solution must be highly memory-efficient (O(1) memory relative to the number of rows) and process the data in a single pass (streaming).

Your objective is to write, compile, and execute a C program that reads a large CSV file and produces a cleaned, resampled, and gap-filled output CSV.

**Input Data:**
File: `/home/user/raw_sensors.csv`
Format: `timestamp,sensor_id,temperature` (no header)
- `timestamp`: Unix timestamp (long integer). The file is strictly sorted by timestamp in ascending order.
- `sensor_id`: Integer from 1 to 5.
- `temperature`: Float.

**Processing Rules:**
1. **Cleaning:** Drop any row where `temperature` is less than `-50.0` or greater than `150.0`.
2. **Deduplication:** For each sensor, if a row has the exact same `timestamp` as the *most recently accepted* row for that specific sensor, drop it.
3. **Resampling:** Aggregate the valid data into 60-second buckets. A bucket's timestamp is calculated as `(timestamp / 60) * 60`. The aggregated value for a bucket is the arithmetic mean of all valid temperatures for that sensor within that 60-second window.
4. **Gap-filling:** The global output time range spans from the bucket of the very first valid row (across all sensors) to the bucket of the very last valid row. 
   - You must output exactly one row per sensor per bucket in this entire range.
   - If a sensor has no valid readings in a bucket, its value should be the same as its value in the *immediately preceding* bucket (forward fill).
   - If a sensor has no preceding bucket data (i.e., a gap occurs before its first valid reading), output `-999.00`.
5. **Output Format:** The output must be written to `/home/user/processed_sensors.csv`.
   - Format: `bucket_timestamp,sensor_id,temperature`
   - Print the temperature rounded to exactly 2 decimal places (e.g., `%.2f`).
   - The output must be sorted by `bucket_timestamp` ascending. Within the same bucket, sort by `sensor_id` ascending (1 to 5).

**Deliverables:**
1. Write your C code to `/home/user/etl.c`.
2. Compile it to `/home/user/etl` using `gcc -O3 /home/user/etl.c -o /home/user/etl`.
3. Run it to generate `/home/user/processed_sensors.csv`.

*Note: You must not load the entire file into memory. Process it as a stream.*