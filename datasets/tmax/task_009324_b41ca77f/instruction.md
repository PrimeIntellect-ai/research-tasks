You are a log analyst investigating application performance patterns. You need to process a raw server access log, clean the data, extract performance features, aggregate them, and load them into a database.

The raw log is located at `/home/user/access.log`. Each line should contain exactly 7 space-separated fields:
`[TIMESTAMP] IP_ADDRESS METHOD ENDPOINT HTTP_VERSION STATUS_CODE RESPONSE_TIME_MS`

However, the log is dirty. You need to write a C++ program (`/home/user/log_analyzer.cpp`) that reads this file and performs the following:

1. **Validation & Cleaning**:
   - Ignore any line that does not have exactly 7 fields.
   - Ignore lines where `METHOD` is not one of: `GET`, `POST`, `PUT`, `DELETE`.
   - Ignore lines where `STATUS_CODE` is not a valid positive integer.
   - Ignore lines where `RESPONSE_TIME_MS` is not a valid non-negative integer (>= 0).

2. **Feature Extraction & Aggregation**:
   For each unique `ENDPOINT` found in the *valid* lines, calculate:
   - `total_requests`: The total number of valid requests.
   - `success_requests`: The number of valid requests where `STATUS_CODE` is exactly `200`.
   - `avg_response_time`: The average `RESPONSE_TIME_MS` of all valid requests for this endpoint. (Compute as integer division, effectively floor/truncating the decimal part).

3. **Output format**:
   Your C++ program should write the aggregated results to a CSV file at `/home/user/endpoint_stats.csv`. 
   - The first line must be the exact header: `endpoint,total_requests,success_requests,avg_response_time`
   - The subsequent lines should list the endpoints sorted alphabetically by the `endpoint` string.

4. **Database Bulk Import**:
   After generating the CSV, use the `sqlite3` command-line tool (ensure it is installed) to create a SQLite database at `/home/user/log_stats.db` and bulk-import the CSV data into a table named `endpoint_stats`. The table schema must treat all numeric columns as `INTEGER` and the endpoint as `TEXT PRIMARY KEY`.

Compile your C++ program using `g++ -std=c++17 -O2 /home/user/log_analyzer.cpp -o /home/user/log_analyzer` and run it to produce the CSV, then perform the SQLite import.