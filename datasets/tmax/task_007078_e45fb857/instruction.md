You are a data analyst tasked with aggregating sensor data from two different international branches of a manufacturing company. The data is stored in two CSV files, but because they originate from different legacy systems, they have different character encodings, timestamp formats, and column names.

Your objective is to write a Python script that reads both files, aligns the timestamps to a common UTC baseline, buckets the data into 1-hour intervals, and calculates the mean measurement value for each hourly bucket.

**Source Data:**
1. `/home/user/branch_eu.csv`
   - Encoding: `iso-8859-1`
   - Columns: `Time,Value,Location`
   - Timestamp format: `YYYY-MM-DD HH:MM:SS+HH:MM` (e.g., `2023-10-01 12:15:00+02:00`)
   
2. `/home/user/branch_na.csv`
   - Encoding: `utf-16`
   - Columns: `Timestamp,Measurement,Site`
   - Timestamp format: `MM/DD/YYYY HH:MM:SS AM/PM-HH:MM` (e.g., `10/01/2023 06:30:00 AM-04:00`)

**Requirements:**
1. Parse the timestamps from both files and convert them to UTC.
2. Group the combined records into 1-hour time buckets based on their UTC time. A bucket should start at the top of the hour (e.g., a reading at `10:15:00 UTC` falls into the `10:00:00` bucket).
3. Calculate the mathematical mean (average) of the values (`Value` / `Measurement`) within each bucket.
4. Output the aggregated results to a new CSV file at `/home/user/summary.csv`.
5. The output file must be `utf-8` encoded and contain exactly two columns: `bucket_utc` and `mean_value`.
6. The `bucket_utc` must be formatted as `YYYY-MM-DD HH:00:00`.
7. The `mean_value` must be formatted as a floating-point number rounded to exactly two decimal places (e.g., `15.00`).
8. The output CSV must be sorted chronologically by `bucket_utc`, starting with the earliest bucket.

Create the python script and run it to produce `/home/user/summary.csv`.