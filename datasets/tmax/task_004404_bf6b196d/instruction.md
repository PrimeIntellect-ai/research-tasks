You are a localization engineer trying to identify when an automated mass-translation script was run by analyzing telemetry logs. You have a log file at `/home/user/telemetry.jsonl` containing JSON-lines data of user interactions. 

However, the telemetry ingestion had a bug: some lines contain malformed unicode escape sequences that cause standard command-line JSON parsers (like `jq`) to fail. 

You must write a C program at `/home/user/detect_anomaly.c` that processes this file, extracts the relevant data, and performs time-based bucketing and anomaly detection. 

Your C program must do the following:
1. Read `/home/user/telemetry.jsonl` line by line.
2. Use POSIX regular expressions (`regex.h`) to:
   - Discard any line that contains the exact substring `"status": "failed"`.
   - Extract the numeric `timestamp` value from lines where `"action": "edit"`. The JSON format will look like: `{"timestamp": 1700000000, "action": "edit", ...}`. 
3. Group the extracted timestamps into 1-hour buckets. A 1-hour bucket is defined mathematically as `bucket_id = timestamp / 3600`. The "start time" of the bucket is `bucket_id * 3600`.
4. Count the number of successful "edit" actions in each 1-hour bucket. Process the buckets in chronological order.
5. Perform Anomaly Detection: Find the **first** 1-hour bucket that represents an anomaly. 
   - An anomaly is defined as a bucket where the edit count is **strictly greater than 3.0 times the mean (average) edit count of all preceding buckets**.
   - To avoid noise, anomaly detection should only begin after at least **5 complete preceding buckets** have been observed. (The 6th bucket is the first one that can be flagged as an anomaly).
6. When the first anomalous bucket is found, write its start time (Unix timestamp) and its count to `/home/user/anomaly_report.txt` in the exact format:
   `ANOMALY_HOUR: <start_timestamp>, COUNT: <count>`
   Then exit the program.

Requirements:
- You must use C and standard libraries (e.g., `stdio.h`, `stdlib.h`, `string.h`, `regex.h`).
- Compile your program using `gcc /home/user/detect_anomaly.c -o /home/user/detect_anomaly` and run it.
- Do not use external libraries (like `jansson` or `cJSON`); rely on `regex.h` or string manipulation to extract the timestamps.