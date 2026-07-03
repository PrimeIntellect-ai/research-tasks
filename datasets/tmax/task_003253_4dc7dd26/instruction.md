You are an AI assistant helping a data scientist clean a dataset corrupted by a buggy ETL pipeline. The ETL job failed and retried multiple times, appending duplicate records to the output file. 

Your task is to write a C program that streams the large dataset, cleans it, deduplicates it, and reshapes it from a "wide" format to a "long" format. 

**Dataset Details:**
- **Input File:** `/home/user/data/etl_dump.csv`
- **Input Format:** `timestamp,temp_sensor,humidity_sensor,pressure_sensor`
- The file has a header row.
- The records are sorted chronologically by `timestamp` (an integer).
- Because of the ETL retries, there are adjacent duplicate records (multiple consecutive rows with the exact same `timestamp`).

**Requirements for the C Program:**
1. **Streaming:** The file is conceptually too large to fit in memory. You must read and process the file line-by-line (streaming).
2. **Deduplication:** For any group of rows with the same `timestamp`, keep ONLY the **first** row encountered and ignore the subsequent duplicates.
3. **Normalization:** Any sensor value that is strictly less than `0.0` must be clamped to `0.00`.
4. **Reshaping (Wide to Long):** Convert each valid row into three separate rows in the output file, one for each sensor.
5. **Output Format:**
   - **Output File:** `/home/user/data/cleaned_long.csv`
   - **Header:** `timestamp,sensor_type,value`
   - `sensor_type` must be exactly one of: `temp`, `humidity`, `pressure`.
   - `value` must be formatted to exactly 2 decimal places (e.g., `20.50`).
   - The output must also be sorted chronologically by timestamp, and for each timestamp, the order of sensors must be `temp`, then `humidity`, then `pressure`.

**Deliverables:**
1. Create your C source code at `/home/user/cleaner.c`.
2. Compile it to `/home/user/cleaner`.
3. Run it so that `/home/user/data/cleaned_long.csv` is successfully generated with the exact specifications above.