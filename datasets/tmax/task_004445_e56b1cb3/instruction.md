You are managing a configuration tracking system. An ETL job that extracts server configuration versions and CPU temperatures has been producing corrupted logs. Due to job retries, it produces duplicate records. Due to temporary agent crashes, there are gaps in the time series. Furthermore, sensor glitches occasionally produce invalid temperatures.

You need to write a C program that cleans, deduplicates, and gap-fills this time-series data. 

The raw data is located at `/home/user/raw_metrics.csv`.
It has no header. The format is: `timestamp,config_version,cpu_temp`
- `timestamp`: Integer (Unix epoch)
- `config_version`: String (up to 10 characters, e.g., "v1.2")
- `cpu_temp`: Float

Write a C program at `/home/user/processor.c`, compile it to `/home/user/processor`, and use it to process the raw data and output the result to `/home/user/clean_metrics.csv`.

Your C program must implement the following logic in this exact order:
1. **Validation**: Ignore (drop) any row where `cpu_temp` is less than `0.0` or greater than `150.0`.
2. **Deduplication**: The input is in chronological order, but retries cause multiple rows with the exact same timestamp. Keep only the *first* valid row for a given timestamp and ignore subsequent rows with the same timestamp.
3. **Gap-filling**: Timestamps are expected exactly every 10 seconds. If there is a missing timestamp (e.g., the previous valid timestamp was 1000, and the current valid timestamp is 1030), you must insert the missing timestamps (1010, 1020) *before* printing the 1030 record. For these inserted records, use the `config_version` of the *last valid record seen*, and set the `cpu_temp` exactly to `0.0`.

Output format:
- Write the cleaned data to `/home/user/clean_metrics.csv` in the exact same format: `timestamp,config_version,cpu_temp`
- Print floats with exactly 1 decimal place (e.g., `%.1f`).

Ensure your program executes successfully and produces the file correctly.