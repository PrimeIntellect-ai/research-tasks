You are a data analyst tasked with processing and unifying environmental sensor data from two different factory floors. The data is currently messy, containing duplicates, missing intervals, and mismatched timestamp formats. 

You need to write a data processing pipeline (using any combination of Python, Bash, AWK, or similar tools) to clean, merge, and resample this data.

**Input Data:**
You have two files located in `/home/user/data/`:
1. `/home/user/data/floor1_temp.csv`
   - Columns: `timestamp_iso,sensor_id,temperature,hash_id`
   - Timestamps are in ISO 8601 format (e.g., `2023-10-01T10:04:22Z`).
2. `/home/user/data/floor2_humidity.csv`
   - Columns: `epoch_ts,device_id,humidity,req_id`
   - Timestamps are Unix epoch integers (e.g., `1696154662`).

**Your objective:**
Generate a single consolidated file at `/home/user/output/merged_environment.csv` that meets the following precise specifications:

1. **Deduplication**: Remove duplicate rows in both datasets based on `hash_id` (for temp) and `req_id` (for humidity). If multiple rows have the same ID, keep only the first one encountered.
2. **Time Bucketing & Aggregation**: 
   - Align all timestamps to UTC.
   - Bucket the data into exactly 15-minute intervals (e.g., `10:00:00`, `10:15:00`, `10:30:00`). A reading belongs to a bucket if its timestamp is `>= bucket_start` and `< bucket_start + 15 mins`.
   - Calculate the average `temperature` and average `humidity` across all sensors/devices for each 15-minute bucket.
3. **Resampling and Gap-Filling**:
   - The final output must have a continuous sequence of 15-minute buckets from strictly `2023-10-01T10:00:00Z` to `2023-10-01T11:45:00Z` inclusive (exactly 8 rows).
   - **Forward Fill**: If a 15-minute bucket has no data for temperature or humidity, carry forward the average value from the most recent previous bucket. 
   - If the very first bucket (`10:00:00Z`) is missing data, leave it blank (empty string `""` or just no characters between commas).
4. **Formatting**:
   - The output file must be a standard CSV with the exact header: `bucket_time,avg_temperature,avg_humidity`
   - `bucket_time` must be in ISO 8601 format (e.g., `2023-10-01T10:15:00Z`).
   - Round numeric averages to exactly 2 decimal places (e.g., `22.50`, `45.33`).

Create the `/home/user/output` directory if it does not exist, and write the final output to `/home/user/output/merged_environment.csv`.