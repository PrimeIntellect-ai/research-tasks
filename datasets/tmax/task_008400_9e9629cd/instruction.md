You are an automation specialist building a data processing pipeline. We have a batch of raw sensor logs that frequently contain duplicate transmissions due to network retries. You need to clean the data, extract features, and detect sudden anomalies (changepoints) in the environment.

Write a Python script at `/home/user/process_pipeline.py` that performs the following steps on the input file `/home/user/input/readings.tsv`:

1. **Hash-Based Deduplication**: 
   Read the TSV file line by line. For each line, compute the SHA-256 hash of the raw string (excluding the trailing newline). Keep only the first occurrence of each unique hash. Discard any subsequent lines that produce a hash you have already seen.

2. **Feature Extraction**:
   The TSV contains three columns separated by tabs: `timestamp` (ISO 8601 string), `device_id` (string), and `payload` (JSON string). 
   Parse the `payload` to extract the `temperature` (float). 
   Group the deduplicated records by `device_id`, and sort the records for each device chronologically by `timestamp`.

3. **Changepoint Detection**:
   For each device, iterate through its sorted, deduplicated records. A "changepoint anomaly" occurs when a temperature reading is **strictly greater** than the arithmetic mean of the **immediately preceding 3 readings** (for that specific device) by **10.0 degrees or more**. 
   *Note: If a device has fewer than 3 preceding readings at a given point, an anomaly cannot be detected yet.*

4. **Output Generation**:
   Find the **first** changepoint anomaly for each device (if any). 
   Write the results to `/home/user/anomalies.json` as a JSON object where the keys are the `device_id`s and the values are the `timestamp`s of their first detected anomaly. Only include devices that actually experienced an anomaly.

Run your script to produce `/home/user/anomalies.json`.