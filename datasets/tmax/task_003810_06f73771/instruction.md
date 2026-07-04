You are a data engineer building a mini-ETL pipeline to process unstructured legacy server logs. 

You have been provided with a raw log file at `/home/user/server_logs.txt`.
Your task is to write a Python script that processes this file, extracts structured information, performs a stratified sampling of the error events, and logs the pipeline's execution metrics.

Here are the specific requirements:

1. **Information Extraction**:
   Parse `/home/user/server_logs.txt`. Some lines represent normal operations, while others represent warnings or errors that contain a specific error code. 
   Lines with error codes always follow this exact format:
   `YYYY-MM-DD HH:MM:SS [SEVERITY] - user:<user_id> - <message>. code:<error_code>`
   *(Example: `2023-10-12 10:05:01 [ERROR] - user:1001 - DB connection lost. code:E-100`)*

   You must extract the `timestamp` (the `YYYY-MM-DD HH:MM:SS` part), `severity`, `user_id`, and `error_code` from every line that contains a `code:`. Ignore lines that do not have an error code.

2. **Data Stratification (Sampling)**:
   We want to inspect a small, balanced sample of errors. Group the extracted error records by their `error_code`. For each unique `error_code`, select exactly the **first 2 chronological occurrences**. If an error code appears fewer than 2 times, include all its occurrences.

3. **Output Generation**:
   Save the stratified samples as a JSON array of objects to `/home/user/stratified_samples.json`.
   Each object must have exactly these keys: `"timestamp"`, `"severity"`, `"user_id"`, and `"error_code"`.
   The final JSON array must be sorted alphabetically by `error_code` in ascending order, and then chronologically by `timestamp` in ascending order.

4. **Pipeline Logging**:
   To monitor the pipeline, create a metrics file at `/home/user/etl_metrics.json`. 
   It must contain exactly one JSON object with the following keys and integer values:
   - `"total_lines_read"`: The total number of lines in the original log file.
   - `"total_errors_parsed"`: The total number of lines that contained an error code and were successfully extracted.
   - `"unique_error_codes"`: The number of distinct error codes found in the file.

Write and execute the Python script to accomplish this.