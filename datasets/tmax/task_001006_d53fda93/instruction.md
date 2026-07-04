You are a data analyst tasked with building a high-performance C++ data pipeline to process incoming CSV telemetry from IoT sensors. The pipeline must filter out malformed or malicious data injections, deduplicate entries, and perform time-based windowed aggregations.

Your task has three phases:
1. **Parameter Extraction:** We received a scanned configuration snippet. Read the image at `/app/specs/params.png` (using `tesseract` or your preferred tool) to extract the pipeline parameters: a secret `SALT` string and an integer `WINDOW` size.
2. **Detector Component:** There is active corruption in the upstream data stream. You must write a bash script `/home/user/detect.sh` that takes a CSV file path as its single argument and prints exactly `CLEAN` if all rows are valid, or `EVIL` if any row is invalid. A row is invalid if `sensor_id` contains any characters other than `[a-zA-Z0-9_]`, or if the float `value` is negative (< 0.0) or absurdly high (> 1000.0). You may write this detector purely in bash/awk or call a compiled C++ binary.
3. **Primary Aggregation Pipeline:** Write a C++ program, compiled to `/home/user/pipeline`, that reads a CSV stream from `stdin`. The CSV format is `timestamp_sec,sensor_id,value` (no headers). The program must:
   - Run the data through your filter (discarding invalid rows).
   - Deduplicate events: An event is a duplicate if the exact string `<timestamp_sec><sensor_id><SALT>` has been seen before (use the SALT from the image).
   - Bucket the remaining valid records by 60-second intervals (e.g., timestamp 125 becomes 120).
   - For each bucket and `sensor_id`, calculate the moving average of the `value` over the current and previous `WINDOW - 1` buckets (using the `WINDOW` extracted from the image).
   - Print the final aggregated output to `stdout` as `bucket_time,sensor_id,moving_avg`.

Ensure `/home/user/detect.sh` and `/home/user/pipeline` are executable and precisely follow the input/output formats described.