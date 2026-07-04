You are a data engineer responsible for building a robust ETL pipeline for a fleet of IoT temperature sensors. The sensors send raw data streams into a centralized log file, but the data is noisy, sometimes duplicated, and arrives out of order. Furthermore, the sensors sometimes drop connections, resulting in missing time intervals.

Your task is to write a purely Bash-based pipeline (using standard tools like `awk`, `sed`, `grep`, `sort`, etc.) to process the raw file and produce a clean, aggregated, gap-filled CSV report. Do not use Python, Perl, or any non-standard scripting languages. 

**Input Data:**
The input file is located at `/home/user/sensor_data.txt`.
The file is pipe-separated with the format: `sensor_id|timestamp|temperature`

**Pipeline Requirements:**

1. **Cleaning:** 
   - Drop any row where the `timestamp` is not exactly a 10-digit integer.
   - Drop any row where the `temperature` is not a valid positive or negative decimal number (e.g., `12.5`, `-4.2`, `10`). Drop rows with letters, empty values, or invalid formats in this field.

2. **Deduplication:**
   - If there are multiple entries with the exact same `sensor_id` and `timestamp`, keep *only* the entry with the highest `temperature` value.

3. **Time-based Bucketing & Aggregation:**
   - Group the cleaned, deduplicated records by `sensor_id` and 1-hour time buckets.
   - A 1-hour bucket is defined by the timestamp integer division by 3600, multiplied by 3600 (i.e., `bucket_start = int(timestamp / 3600) * 3600`).
   - Calculate the arithmetic mean of the temperatures for each sensor in each bucket. 
   - Round the average temperature to exactly 1 decimal place (e.g., `21.3`).

4. **Resampling / Gap-Filling:**
   - For each unique `sensor_id` present in the *cleaned* data, identify the minimum and maximum `bucket_start` times.
   - For every 1-hour interval (3600 seconds) between the sensor's minimum and maximum bucket times (inclusive), ensure a row exists.
   - If a bucket has no data in the cleaned records, output `0.0` as the average temperature for that gap.

5. **Sorting and Output:**
   - The final output must be saved to `/home/user/etl_output.csv`.
   - The format must be comma-separated: `sensor_id,bucket_start_time,avg_temperature`
   - Sort the final output alphabetically by `sensor_id` (ascending), and then numerically by `bucket_start_time` (ascending).

Ensure your resulting file strictly matches these rules.