You are an automation specialist maintaining a data pipeline. A recent ETL job ran multiple times due to network retries, causing duplicate records to be ingested into our raw logs directory in multiple formats. 

Your task is to write and execute a Python script (`/home/user/etl_dedup.py`) that processes these raw files, standardizes the fields, removes duplicates, and outputs a clean Parquet file.

Here are the requirements:

1. **Input Data**: 
   - Directory: `/home/user/raw_logs/`
   - Formats: The directory contains both CSV files (with headers `id,time,text`) and JSON files (containing a list of objects with keys `id`, `time`, `text`).
   
2. **Data Transformation & Normalization**:
   - **`id`**: Must be cast to an integer.
   - **`time`**: The timestamps are either Unix epoch integers (seconds) or ISO 8601 strings (e.g., `2021-06-01T00:00:00Z`). Convert all timestamps to integer Unix epoch seconds.
   - **`text`**: Normalize the text by converting it to lowercase and removing ALL characters except alphanumeric characters (a-z, 0-9) and spaces. Multiple contiguous spaces should be reduced to a single space, and leading/trailing spaces should be stripped.

3. **Deduplication**:
   - Two records are considered duplicates if they have the exact same `id` AND the same normalized `time` (Unix timestamp).
   - If duplicates are found, keep only one of them. (It does not matter which one, as the `text` should be identical after normalization).

4. **Output**:
   - Write the cleaned, deduplicated dataset to `/home/user/clean_logs.parquet`.
   - The Parquet file must contain exactly three columns: `id` (int64), `time` (int64), and `text` (string).
   - The records in the Parquet file must be sorted by `time` in ascending order, and then by `id` in ascending order.

You may need to install libraries like `pandas` and `pyarrow`. Ensure your script runs successfully and generates the required Parquet file.