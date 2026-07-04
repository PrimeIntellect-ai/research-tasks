You are a data analyst dealing with a corrupted log file containing user search queries. The system that exported the data had a bug where unicode escape sequences (`\uXXXX`) were sometimes truncated or malformed, causing downstream JSON parsers to break. 

Your task is to write a C++ program that processes a CSV file of logs, detects malformed escape sequences, and performs time-based and windowed aggregations with a quality gate.

**Input File:** `/home/user/raw_logs.csv`
**Format:** `timestamp_sec,user_id,query_text` (Headers are included in the first row).
*   `timestamp_sec`: Integer UNIX timestamp.
*   `user_id`: String (no commas).
*   `query_text`: String (may contain spaces, but no commas or newlines).

**Processing Requirements:**
1.  **Time-based Bucketing:** Group the logs into 300-second (5-minute) tumbling windows based on `timestamp_sec`. A bucket starts at a multiple of 300. For example, timestamp `305` belongs to the bucket starting at `300`.
2.  **String Validation (Malformed Detection):** 
    *   Scan `query_text` for the literal sequence `\u`.
    *   If `\u` is found, the immediately following 4 characters must be valid hexadecimal digits (`0-9`, `a-f`, `A-F`). 
    *   If the string ends before 4 characters are available, or if any of those 4 characters are not valid hex digits, the *entire row* is marked as **malformed**.
3.  **Aggregation:** For each 300-second bucket that contains *at least one row*, calculate:
    *   `query_count`: The total number of rows in the bucket (including malformed ones).
    *   `rolling_avg_length`: A rolling average of the raw string length (`std::string::length()`) of `query_text`. This rolling average should cover the current bucket and the *up to two* previous consecutive buckets (i.e., a 3-bucket window). Note: Include a previous bucket in the window *only if it contained data*. If a bucket is empty, it does not count towards the window. Calculate this as `(sum of lengths in window) / (total rows in window)`. Round down to the nearest integer.
4.  **Quality Gate:** If the ratio of malformed rows to total rows in a given bucket is strictly greater than `0.05` (5%), the bucket's status is `FLAGGED`. Otherwise, the status is `OK`.

**Output:**
Write the results to `/home/user/aggregated_stats.csv` with the following header:
`bucket_start_ts,query_count,rolling_avg_length,status`

Sort the output chronologically by `bucket_start_ts` in ascending order.

**Constraints & Notes:**
*   Write your solution in C++ (save it as `/home/user/process_logs.cpp`).
*   Compile it using standard tools available on Linux (e.g., `g++ -std=c++17 process_logs.cpp -o process_logs`).
*   Execute your program to generate the final `aggregated_stats.csv` file. 
*   Do not change the headers or output format.