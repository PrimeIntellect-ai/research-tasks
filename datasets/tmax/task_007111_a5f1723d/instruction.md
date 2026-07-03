You are a data analyst monitoring system performance. You have a raw CSV file containing time-series system metrics at `/home/user/system_metrics.csv`. You need to write a C++ program to process this stream, identify anomalous shifts in system behavior, and log them.

The CSV file has the following header and format:
`timestamp,cpu,mem,net_in,net_out`
- `timestamp`: Integer UNIX epoch time.
- `cpu`: Float, CPU usage percentage (0.0 to 100.0).
- `mem`: Float, memory usage in MB.
- `net_in`: Float, network traffic in KB/s.
- `net_out`: Float, network traffic in KB/s.

Write a C++ program at `/home/user/detector.cpp` that performs the following:
1. **Time-based Bucketing**: Group the data into 60-second buckets. A bucket's index is calculated as `timestamp / 60`. The bucket's start time is `bucket_index * 60`.
2. **Aggregation**: For each bucket, calculate the average (mean) value for `cpu`, `mem`, `net_in`, and `net_out`. Note: Some buckets might be empty; skip them and only compare consecutive non-empty buckets in the data stream.
3. **Normalization**: To compare these disparate metrics, normalize the average values for each bucket:
   - Normalized CPU = `average_cpu / 100.0`
   - Normalized Mem = `average_mem / 16000.0`
   - Normalized NetIn = `average_net_in / 1000.0`
   - Normalized NetOut = `average_net_out / 1000.0`
4. **Distance & Anomaly Detection**: For each non-empty bucket (starting from the second available bucket), compute the Euclidean distance between its normalized feature vector and the *previous* non-empty bucket's normalized feature vector.
   - Euclidean distance $d = \sqrt{\Delta cpu^2 + \Delta mem^2 + \Delta net\_in^2 + \Delta net\_out^2}$
   - An anomaly is detected if $d > 0.4$.
5. **Logging**: When an anomaly is detected, append a log line to `/home/user/anomalies.log` in the exact following format:
   `[LOG] Anomaly detected at bucket {bucket_start_timestamp}: distance={d}`
   Round the distance to exactly 4 decimal places (e.g., `0.5120`).

Compile your C++ program and execute it so that `/home/user/anomalies.log` is generated.