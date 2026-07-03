You are a data scientist working with a raw system log file that was exported as a CSV. Unfortunately, the export process was flawed: the logs contain embedded newlines within text fields, mixed or invalid UTF-8 byte sequences, and duplicate entries. 

Your task is to write a Python script that processes this dataset, cleans it, extracts specific information using regular expressions, and computes hourly summary statistics. 

Here are the specific requirements:

**Input Data:**
- File: `/home/user/raw_logs.csv`
- Columns: `tx_id`, `timestamp`, `user_id`, `response_time_ms`, `message`

**Processing Steps:**
1. **Character Encoding:** Read the CSV file such that any invalid UTF-8 characters in the file are replaced with the standard Unicode replacement character (`\ufffd`) rather than causing a decoding error.
2. **CSV Parsing:** Correctly parse the CSV. Be careful: the `message` column frequently contains embedded newline characters (`\n`), so simple line-by-line reading (like `readlines()`) will corrupt the data. You must use a robust CSV parser.
3. **Deduplication:** Remove duplicate records based on the `tx_id` column. If multiple rows have the same `tx_id`, keep only the **first** one encountered in the file.
4. **Data Cleaning:** Drop any rows where `response_time_ms` is less than `0` (these are logging errors).
5. **Regex Extraction:** Use a regular expression to search the `message` column for error codes matching the exact pattern `ERR-` followed by exactly three digits (e.g., `ERR-404`, `ERR-500`). If multiple error codes exist in a single message, extract only the first one. If none exist, treat the extracted error code as null/None.
6. **Time-based Bucketing:** Truncate the `timestamp` (which is in ISO 8601 format, e.g., `2023-10-15T14:32:05Z`) down to the hour (e.g., `2023-10-15T14:00:00Z`).
7. **Aggregation:** Group the cleaned, deduplicated data by the hourly time bucket. For each hour, calculate:
   - `transaction_count`: The total number of valid transactions in that hour.
   - `unique_users`: The count of distinct `user_id`s in that hour.
   - `avg_response_time_ms`: The mean response time, rounded to exactly 2 decimal places.
   - `error_counts`: A dictionary/object mapping each extracted error code to its frequency in that hour. Do not include null/None in this dictionary.

**Output:**
Write the final aggregated data to a JSON file at `/home/user/hourly_summary.json`. 
The JSON must be a list of objects, sorted chronologically by `hour_bucket`.
The structure must look exactly like this:
```json
[
  {
    "hour_bucket": "2023-10-15T14:00:00Z",
    "transaction_count": 45,
    "unique_users": 12,
    "avg_response_time_ms": 150.25,
    "error_counts": {
      "ERR-404": 3,
      "ERR-500": 1
    }
  }
]
```

Write and execute your Python script to produce the target JSON file.