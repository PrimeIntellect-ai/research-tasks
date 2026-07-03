As an automation specialist, I need you to create a C++ data processing tool to handle industrial IoT temperature sensor logs. 

We have a raw sensor data file located at `/home/user/sensor_data.csv`. The file has no header and contains comma-separated values in the following format:
`timestamp,sensor_id,temperature`
(e.g., `1700000005,S1,22.5`)
The timestamp is in UNIX epoch seconds.

Your objective is to write a C++ program (using only the C++ standard library, compile it with `g++ -std=c++17`) and save the source code to `/home/user/processor.cpp`. Compile it to an executable named `/home/user/sensor_processor`. 

When run, the executable must perform the following pipeline steps:
1. **Time-based Bucketing**: Group the readings into 60-second tumbling windows (buckets) aligned to the epoch (e.g., bucket `1700000000` covers timestamps `1700000000` to `1700000059` inclusive).
2. **Feature Extraction**: Calculate the `mean`, `max`, and `min` temperature for each bucket.
3. **Anomaly Detection**: Compare the `mean` of the current bucket with the `mean` of the *chronologically previous* bucket (only consider buckets that have data; ignore empty buckets). If the absolute difference in the mean temperature is strictly greater than `5.0` degrees, flag the current bucket as an anomaly. The first bucket chronologically can never be an anomaly.
4. **Data Output**: Write the results to `/home/user/processed_stats.csv` with a header row exactly as:
`bucket_start,mean,max,min,is_anomaly`
Followed by the data rows sorted chronologically by `bucket_start`. Format floating-point numbers to exactly 1 decimal place. `is_anomaly` should be `1` if an anomaly was detected, `0` otherwise.
5. **Pipeline Logging**: The program must append log entries to `/home/user/pipeline.log` during execution. The log must contain exactly these lines:
- `[INFO] Pipeline started`
- `[INFO] Processed <N> valid records` (where `<N>` is the total number of lines read)
- `[WARN] Detected <M> anomalies` (where `<M>` is the total number of anomalies found)
- `[INFO] Pipeline completed`

Write the C++ program, compile it, and run it to produce `/home/user/processed_stats.csv` and `/home/user/pipeline.log`.