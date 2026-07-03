You are a log analyst investigating user activity patterns across different regions. A downstream pipeline has been failing silently, dropping log entries because the raw logs contain embedded newlines within quoted message fields, and the file uses a specific encoding that breaks naive Unix tools.

Your task is to write a Python script `/home/user/process_logs.py` to correctly parse and reshape these logs, and then serve the results.

Here are the requirements:
1. **Input File:** You have a raw log file at `/home/user/raw_chat_logs.csv`. It is encoded in `UTF-16LE`.
2. **Data Cleaning:** 
   - Parse the CSV correctly, preserving rows with embedded newlines in the `message` column.
   - Drop any rows where the `message` column is completely empty.
3. **Time-based Bucketing:** 
   - The `timestamp` column is in the format `YYYY-MM-DD HH:MM:SS`.
   - Truncate the timestamps to the hour (e.g., `2023-10-24 14:15:00` becomes `2023-10-24 14:00`).
4. **Reshaping (Wide Format):**
   - Aggregate the data to count the number of valid messages per `region` per `hour`.
   - Reshape the data into a wide format where:
     - Each row represents a unique `hour` (sorted chronologically).
     - Columns represent each unique `region` found in the data.
     - Values are the message counts (fill missing combinations with 0).
5. **Output:**
   - Save the wide-format data as a JSON file at `/home/user/hourly_region_counts.json`. It must be a list of dictionaries (e.g., `[{"hour": "2023-10-24 14:00", "EU": 5, "ASIA": 0}, ...]`).
   - Save the exact same DataFrame to a Parquet file at `/home/user/hourly_region_counts.parquet`.
6. **Serving:**
   - After creating the files, start a simple Python HTTP server in the background on port `8080` serving the `/home/user` directory so the files can be downloaded.

Execute the tasks in the terminal. You may install any Python packages you need (e.g., `pandas`, `pyarrow`).