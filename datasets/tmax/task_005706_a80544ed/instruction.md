I need you to act as a data analyst and process a raw server log CSV file into aggregated time-series metrics. 

You will find the input data at `/home/user/server_logs.csv`. 
It contains four columns: `timestamp` (ISO 8601 format), `endpoint` (string), `response_time_ms` (float), and `status_code` (integer).

Please write and run a Python script to perform the following tasks:
1. **Time-based Bucketing**: Group the log records into 5-minute tumbling windows (intervals) based on the `timestamp`. The bucket time should represent the start of the 5-minute interval (e.g., `2023-10-01T10:00:00Z` covers up to `2023-10-01T10:04:59Z`).
2. **Feature Extraction / Aggregation**: For each 5-minute bucket, calculate:
   - `request_count`: The total number of requests in that window.
   - `avg_response_time`: The mean response time in milliseconds, rounded to 2 decimal places.
   - `error_rate_pct`: The percentage of requests that resulted in an error (status_code >= 400), rounded to 2 decimal places (e.g., 15.50).
3. **Save the Output**: Write the aggregated data to a new CSV file at `/home/user/metrics_5min.csv`. The file must have a header row (`bucket_time,request_count,avg_response_time,error_rate_pct`) and be sorted chronologically by `bucket_time` in ascending order.
4. **Pipeline Logging**: As part of your Python script, append a single line to a log file located at `/home/user/pipeline.log`. The line must exactly match this format:
   `SUCCESS - Processed <N> input rows. Generated <M> output buckets.`
   (Replace `<N>` and `<M>` with the actual integer counts).

You may use standard Python libraries or `pandas` to complete this task. Please ensure your code executes successfully and produces the two required files (`metrics_5min.csv` and `pipeline.log`).