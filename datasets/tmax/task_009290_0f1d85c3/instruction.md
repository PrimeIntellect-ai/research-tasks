You are an ETL data engineer troubleshooting a failed pipeline. A data ingestion job crashed and retried multiple times, resulting in a raw data dump that contains duplicate records, noisy/invalid outliers, and missing time intervals.

You need to write a C program that cleans, aggregates, and gap-fills this time-series data. 

The raw data is located at `/home/user/raw_telemetry.csv`. It has no header, and each line contains `timestamp,value` (where timestamp is an integer UNIX epoch, and value is a float).

Write and execute a C program that performs the following pipeline steps:

1. **Validation Checkpoint (Quality Gate):** Read the CSV and silently discard any rows where the value is strictly less than `-50.0` or strictly greater than `150.0`.
2. **Resampling & Aggregation:** 
   - Group the valid records into 10-second buckets. A bucket's time is defined as `(timestamp / 10) * 10` (using integer division).
   - If multiple valid records fall into the same 10-second bucket (due to the ETL retries), compute the average of their values to represent that bucket.
3. **Interpolation & Gap-filling:**
   - Determine the minimum bucket time (`min_bucket`) and maximum bucket time (`max_bucket`) from the valid data.
   - For every 10-second interval from `min_bucket` to `max_bucket` inclusive, generate a data point.
   - If a bucket has no valid data (an empty gap), fill it using linear interpolation between the nearest non-empty buckets before and after it. 
4. **Summary Statistics:**
   - Compute the Minimum, Maximum, and Mean of the *final gap-filled time series*.

**Outputs required:**
1. `/home/user/processed_telemetry.csv`: The gap-filled time series.
   - Format: `bucket_time,interpolated_value`
   - Float precision: strictly 2 decimal places (e.g., `1010, 13.50`).
   - Order: Chronological.
2. `/home/user/summary.txt`: The summary statistics of the final series.
   - Format exact match required:
     ```
     MIN: [value]
     MAX: [value]
     MEAN: [value]
     ```
   - Float precision: strictly 2 decimal places (e.g., `19.58`).

You may use standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, etc.). Compile and run your code to produce the final output files.