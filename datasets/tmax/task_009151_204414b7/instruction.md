You are a data engineer tasked with building an ETL pipeline to process IoT sensor telemetry data. You need to write a Go program that processes an input CSV and extracts anomalies based on a rolling window algorithm.

You have been provided with a raw sensor dataset at `/home/user/sensor_data.csv` containing the columns: `timestamp`, `vibration`, `temperature`.
The dataset is chronologically sorted by timestamp, but it contains duplicate rows due to transmission errors.

Write a Go script (e.g., at `/home/user/process.go`) and run it to produce a processed JSON Lines file at `/home/user/processed_data.json`.

Your Go program must perform the following pipeline steps:
1. **Hash-Based Deduplication**: Read the CSV. Deduplicate the rows by computing a SHA-256 hash of the entire raw CSV line (exactly as it appears in the file, excluding the newline character). Keep only the first occurrence of each unique line. 
2. **Global Min-Max Normalization**: After deduplication, find the global minimum and maximum values of the `vibration` column. Create a normalized vibration series where values are scaled between 0.0 and 1.0 using the formula: `(vibration - min) / (max - min)`.
3. **Windowed Aggregation**: Calculate a Simple Moving Average (SMA) of the *normalized* vibration values over a rolling window of the last 3 data points (including the current point). For the first two points, calculate the average using only the available points (i.e., window of 1, then window of 2).
4. **Distance & Anomaly Detection**: An anomaly is flagged if the absolute difference between the current point's normalized vibration and the SMA for that point is strictly greater than `0.3`.

**Output Format Requirements**:
Write the results to `/home/user/processed_data.json` where each line is a JSON object containing exactly two keys:
- `timestamp`: The timestamp string from the CSV.
- `is_anomaly`: A boolean (`true` or `false`) based on step 4.

The output should retain the chronological order of the deduplicated dataset. Do not include the CSV header in your output JSON file. Run your Go program so the final file is generated.