You are a data engineer responsible for building robust ETL pipelines. We recently had an issue where a naive shell script processing system logs silently dropped data because the log messages contained embedded newlines. 

Your task is to write a robust Python ETL script that correctly processes this CSV, extracts structured information from the messy multiline text, aggregates the data into time buckets, and outputs a strict validation checkpoint.

**Input Data:**
There is a CSV file located at `/home/user/data/input.csv` with the following columns:
1. `timestamp` (ISO8601 format, e.g., `2023-10-01T14:12:33Z`)
2. `level` (`INFO`, `WARN`, `ERROR`, `DEBUG`)
3. `message` (A text message that often spans multiple lines and contains embedded newline characters `\n`. It is properly quoted according to RFC 4180).

**Requirements:**
1. Create a Python script at `/home/user/etl_pipeline.py`.
2. The script must read `/home/user/data/input.csv` without dropping or corrupting rows that contain embedded newlines. (Do not count the header as a data row).
3. Filter the dataset to include *only* rows where `level` is exactly `ERROR`.
4. **Information Extraction**: Scan the `message` column of the filtered rows to extract an error code using the following pattern: the literal string `ErrorCode:` followed by optional whitespace, followed by a code consisting of exactly 3 uppercase letters, a hyphen, and 4 digits (e.g., `ErrorCode: SYS-1029` or `ErrorCode:APP-0001`). 
   - If a message contains multiple codes, only extract the first one.
   - If a message does not contain a matching code, ignore it for the aggregation step, but it still counts as an `ERROR` row.
5. **Time Bucketing and Aggregation**: Group the extracted error codes into 1-hour time buckets based on the `timestamp` column. The time bucket should be formatted as `YYYY-MM-DDTHH` (e.g., `2023-10-01T14`). Calculate the frequency of each error code within each hourly bucket.
6. **Outputs**: 
   - Ensure the output directory `/home/user/output/` exists.
   - Write the aggregated data to `/home/user/output/hourly_errors.json`. The JSON should be a dictionary mapping the time bucket string to another dictionary of `errorCode: count` pairs. (e.g., `{"2023-10-01T14": {"SYS-1029": 2, "DBX-9999": 1}}`).
   - **Quality Gate / Validation Checkpoint**: Write a validation metadata file to `/home/user/output/checkpoint.json` containing exactly the following keys:
     - `"total_logical_rows"`: Integer count of all data rows successfully read from the CSV (excluding the header).
     - `"error_rows_found"`: Integer count of rows where `level == "ERROR"`.
     - `"extracted_codes_count"`: Integer count of `ERROR` rows that successfully yielded a valid error code.
7. Run your script to generate the output files. The script should exit with a status code of 0.