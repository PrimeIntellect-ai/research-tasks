You are a data scientist tasked with cleaning up time series data from a flaky ETL pipeline. The ETL job failed and retried several times, resulting in multiple output files in different formats with overlapping, duplicate, and slightly out-of-sync records (timestamp jitter).

You have been given a directory `/home/user/data/` containing two files:
1. `run_1.csv`: A CSV file containing initial data.
    Columns: `ts` (Unix epoch timestamp in seconds), `sensor_a` (float), `sensor_b` (float)
2. `retry_1.json`: A JSON lines file containing retry data.
    Keys: `datetime` (ISO 8601 string, various timezones), `val_a` (float), `val_b` (float)

Your objective is to write and execute a Python script that performs the following steps:
1. Load both files into a single unified dataset.
2. Normalize all timestamps to UTC.
3. Clean and Deduplicate:
   - Round the UTC timestamps to the nearest whole second.
   - Group the records by this rounded UTC timestamp.
   - For each group, compute the mean of the sensor A values and sensor B values (ignore nulls in the mean calculation).
   - Drop any resulting grouped records where either the average sensor A or average sensor B is null/missing.
   - Sort the resulting dataset chronologically.
4. Compute Similarity:
   - Calculate the overall Euclidean distance between the aligned `sensor_a` and `sensor_b` arrays across the entire cleaned dataset.
5. Output:
   - Save the cleaned time series to `/home/user/cleaned_data.csv`. The CSV must have exactly three columns in this order: `timestamp` (ISO 8601 string with 'Z' denoting UTC, e.g., `2023-10-01T12:00:00Z`), `sensor_a`, `sensor_b`. Both sensor values should be rounded to 3 decimal places.
   - Save the computed Euclidean distance to `/home/user/distance.txt`, rounded to 2 decimal places (e.g., `14.52`).

You may install and use standard data science libraries (like `pandas` and `numpy`) using `pip`.