You are a data engineer working on an ETL pipeline written in C. We have a recurrent issue where our ingestion job sometimes retries and appends duplicate records into our time-series storage file. 

Your task is to write a C program that safely ingests new wide-format time-series data, reshapes it to long-format, filters out anomalous data (validation), and ensures no duplicate records are appended to the existing output file.

**Source Data:** `/home/user/raw_data.csv`
Format: `timestamp,sensor_1_temp,sensor_2_temp` (Headerless)
*Note: The timestamp is a Unix epoch integer. The temperatures are floats.*

**Destination Data:** `/home/user/processed_data.csv`
Format: `timestamp,sensor_id,temperature` (Headerless)
*Note: `sensor_id` should be `1` for sensor_1_temp and `2` for sensor_2_temp. `temperature` should be printed to 1 decimal place.*

**Requirements:**
1. **Reshape:** Convert the wide format from `raw_data.csv` into the long format required for `processed_data.csv`. Each row in the raw file will yield up to two rows in the processed file.
2. **Quality Gates:** Any temperature reading strictly less than `-40.0` or strictly greater than `85.0` is physically impossible for our sensors and must be discarded. Do not append these invalid readings.
3. **Idempotency (Deduplication):** Read the existing `/home/user/processed_data.csv` file before processing. If a `(timestamp, sensor_id)` pair already exists in the destination file, **do not** append it again. 
4. **Output:** Append valid, non-duplicate records to `/home/user/processed_data.csv`.
5. **Implementation:** Write your C code in `/home/user/etl.c`. Compile it to `/home/user/etl` and run it. You may assume timestamps fit within standard 32/64-bit integers and the files will not exceed a few megabytes.

Compile your code with `gcc -O2 -o /home/user/etl /home/user/etl.c` and execute it.