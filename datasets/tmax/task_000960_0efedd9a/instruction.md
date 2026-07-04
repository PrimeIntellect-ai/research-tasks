You are an automation specialist building a data processing pipeline for telemetry logs. We have a pipeline that ingests JSON-lines log files, cleans them, imputes missing values, flags anomalies, and loads the data into a database.

Currently, the pipeline is broken because our C-based JSONL parser fails on unicode escape sequences, and we lost the original anomaly detection regex (we only have a screenshot of it).

Your task is to build and run the end-to-end pipeline:

1. **Extract Regex from Image:**
   There is an image of the anomaly detection specification at `/app/regex_spec.png`. Use `tesseract` to extract the regex pattern from this image. (Note: The regex will be used to identify anomalous log messages).

2. **Fix and Extend the C Data Cleaner:**
   We have a partial C program at `/app/json_cleaner.c` that reads `/app/raw_logs.jsonl`. The JSONL has the following schema: `{"id": int, "timestamp": "string", "message": "string", "sensor_val": float}`.
   You must fix and complete the C program so that it:
   - Correctly parses and unescapes standard Unicode escape sequences (e.g., `\uXXXX`) in the `message` field into valid UTF-8.
   - Performs data imputation: if `sensor_val` is missing or null, impute it using **forward-fill** (use the last seen valid `sensor_val`). Assume the first row always has a valid `sensor_val`.
   - Outputs the cleaned data as a standard CSV file to `/home/user/cleaned.csv` with the header: `id,timestamp,message,sensor_val`.

3. **Filter Anomalies:**
   Using the regex extracted in step 1, scan the `message` column of `/home/user/cleaned.csv` using Bash utilities (e.g., `grep`, `awk`).
   Extract the `id` of every row that matches the regex. Save these IDs (one per line) to `/home/user/anomaly_ids.txt`.

4. **Database Bulk Import:**
   Using `sqlite3`, bulk import the `/home/user/cleaned.csv` file into an SQLite database at `/home/user/telemetry.db`. The table should be named `logs`.

Ensure your C program is compiled efficiently and the final files `/home/user/cleaned.csv`, `/home/user/anomaly_ids.txt`, and `/home/user/telemetry.db` are generated. Your extraction of the anomalies will be graded based on an F1 score against a hidden ground truth.