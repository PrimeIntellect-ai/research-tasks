You are acting as a log analyst investigating performance degradation in our authentication service. You need to process a raw log file, compute some specific time-based metrics, and generate an alert report.

Write a C++ program to process `/home/user/input_logs.jsonl`. Each line in this file is a JSON object.

Your C++ program must perform the following data processing pipeline:

1. **Multi-format & Validation:**
   Read the file line by line. You must only process "valid auth requests". A valid auth request is defined as a JSON object where:
   - `svc` equals exactly `"auth"`
   - `status` is an integer between `200` and `599` inclusive.
   - It contains valid `ts` (integer Unix timestamp) and `rt` (integer response time in ms) fields.
   Ignore any lines that do not meet these constraints or have malformed JSON. 

2. **Time-based Bucketing:**
   Group the valid auth requests into 1-minute buckets based on their `ts` field. A bucket's timestamp is the `ts` rounded down to the nearest multiple of 60.

3. **Rolling Statistics Computation:**
   For each minute bucket, calculate:
   - `bucket_avg`: The average response time (`rt`) of all valid auth requests strictly within this bucket.
   - `rolling_avg`: The simple moving average of the response times of the **last 3 valid auth requests** processed up to and including the last chronological request in this bucket. (If fewer than 3 valid auth requests have been processed in total by the end of the bucket, average whatever is available).
   *Note: Both averages should be computed as integer division (truncate decimal).*

4. **Multi-format Export (CSV & Template Generation):**
   - **CSV Export:** Write a CSV file to `/home/user/bucket_stats.csv` with exactly this header: `bucket_ts,count,bucket_avg,rolling_avg`. Add a row for each minute bucket that contains at least one valid auth request, sorted by `bucket_ts` ascending.
   - **Alert Generation:** Read the template file located at `/home/user/alert_template.txt`. For every bucket where `bucket_avg >= 500`, replace the placeholders in the template and append the result to `/home/user/alerts.md`. Separate each alert block with a blank line. 

Placeholders in `/home/user/alert_template.txt` to replace:
- `{{ts}}` -> `bucket_ts`
- `{{avg}}` -> `bucket_avg`
- `{{rolling}}` -> `rolling_avg`
- `{{count}}` -> number of valid auth requests in the bucket

To compile your code, you can use `g++`. Note: C++ does not have a built-in JSON parser, but you can download the popular `nlohmann/json` single-header library to `/home/user/json.hpp` via `wget https://raw.githubusercontent.com/nlohmann/json/develop/single_include/nlohmann/json.hpp` and include it in your project.

Once your C++ program has successfully run and generated `/home/user/bucket_stats.csv` and `/home/user/alerts.md`, the task is complete.