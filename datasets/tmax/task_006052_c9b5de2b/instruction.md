You are a log analyst investigating sudden latency spikes across a globally distributed application. You have received raw log files from three different regional servers. Due to misconfigurations, the logs have different character encodings, varying timestamp formats, and different units for response times.

Your task is to write a script (in any language you choose) to process these logs, standardize them, compute rolling statistics, and detect anomalies.

**Input Data:**
The raw logs are located in `/home/user/raw_logs/`. There are three files:
1. `/home/user/raw_logs/server_eu.log`:
   - Encoding: ISO-8859-1
   - Format: `DD/MM/YYYY HH:mm:ss | status | response_time`
   - Unit for response_time: milliseconds (ms)
2. `/home/user/raw_logs/server_us.log`:
   - Encoding: UTF-8
   - Format: `YYYY-MM-DDTHH:mm:ssZ | status | response_time`
   - Unit for response_time: seconds (s)
3. `/home/user/raw_logs/server_asia.log`:
   - Encoding: UTF-16LE
   - Format: `Epoch_milliseconds | status | response_time`
   - Unit for response_time: microseconds (us)

**Processing Requirements:**
1. **Normalization & Encoding:** Read all three log files, correctly handling their specific character encodings. Standardize all timestamps to Unix Epoch Seconds. Standardize all response times to milliseconds (ms) as floating-point numbers.
2. **Time-based Bucketing:** Combine all log entries and group them into 5-minute (300 seconds) tumbling windows (buckets). A bucket's start time should be a multiple of 300 (e.g., if a log is at Epoch `1696154530`, it belongs to the bucket starting at `1696154400`).
3. **Aggregation:** For each 5-minute bucket, calculate the mean response time (in ms) across all servers.
4. **Anomaly Detection:** Sort the buckets chronologically by start time. An anomaly is detected if a bucket's mean response time is strictly greater than **2.5 times** the mean response time of the *immediately preceding* bucket. (Note: The very first chronological bucket cannot be an anomaly since it has no preceding bucket).

**Output:**
Create a CSV file at `/home/user/anomalies.csv` containing the detected anomalies. The CSV must have exactly this header: `bucket_start_epoch,avg_latency_ms,prev_avg_latency_ms`.
Format the floating-point values to exactly 2 decimal places. 

If your script requires external dependencies (like `pandas`), you are responsible for installing them in your user environment.