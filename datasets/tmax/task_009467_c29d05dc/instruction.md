You are a data engineer tasked with building a fast ETL pipeline. An upstream system exposes a directory of sensor logs via an HTTP server. You need to fetch these logs, process them in parallel, bucket the data by hour, and aggregate the maximum sensor values.

Here are your specific instructions:

1. **Data Ingestion (Local-Remote Transfer):**
   A local HTTP server is running on `http://localhost:8080/`. It hosts an index of JSON files containing sensor data.
   Download all the `.json` files from `http://localhost:8080/` into a local directory called `/home/user/raw_data`. (You will need to create this directory).

2. **Parallel Processing & Aggregation (Time-based Bucketing):**
   Write a Python script at `/home/user/etl.py` that reads all downloaded JSON files in `/home/user/raw_data`. 
   - The script **must** process the files in parallel using Python's `multiprocessing` or `concurrent.futures` module (simulate a scenario where I/O and parsing is a bottleneck).
   - Each JSON file contains an array of records in the format: `{"timestamp": "YYYY-MM-DDTHH:MM:SSZ", "value": float}`.
   - Extract the timestamp and truncate it to the start of the hour (e.g., `2023-11-15T14:32:10Z` becomes `2023-11-15T14:00:00Z`).
   - Find the maximum `value` for each hourly bucket across *all* files.

3. **Output:**
   Write the aggregated results to a CSV file at `/home/user/hourly_max.csv`.
   - The CSV should have no header row.
   - The format must be exactly: `YYYY-MM-DDTHH:00:00Z,MAX_VALUE`
   - The `MAX_VALUE` should be formatted to one decimal place (e.g., `45.2`).
   - The rows must be sorted chronologically by the hour bucket.

Run your script to produce the final `/home/user/hourly_max.csv`.