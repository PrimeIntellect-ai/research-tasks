You are a data engineer troubleshooting an ETL pipeline. Due to a faulty retry mechanism, our pipeline has ingested duplicate sensor readings into our raw storage. To make matters worse, the retried records aren't exact duplicates—they contain slight floating-point noise in the sensor values.

Your task is to write a Python script that processes a large CSV file of sensor data, deduplicates the noisy retries, and aggregates the results.

**Input Data:**
File: `/home/user/raw_sensor_data.csv`
Columns: `timestamp` (ISO8601 format, e.g., `2023-10-01T12:05:23Z`), `sensor_id` (string), `x` (float), `y` (float)

**Processing Requirements:**
1. **Time-based Bucketing**: Group the records into 1-minute buckets based on the `timestamp` (e.g., any time from `12:05:00` to `12:05:59` falls into the `2023-10-01T12:05:00Z` bucket).
2. **Streaming/Ordered Processing**: Process records within each bucket in the exact order they appear in the file.
3. **Similarity Deduplication**: For a given `sensor_id` within a 1-minute bucket, a record is considered a "noisy duplicate" if its Euclidean distance to *any previously accepted record* in the same bucket and sensor is less than or equal to `0.1`. 
   *(Distance formula: `sqrt((x2 - x1)^2 + (y2 - y1)^2)`)*
   If a record is a duplicate, drop it. Otherwise, add it to the list of accepted records for that bucket.
4. **Aggregation**: After deduplication, calculate the arithmetic mean of `x` and `y` for all accepted records per `sensor_id` per 1-minute bucket. Round the means to 4 decimal places.

**Output:**
Write the aggregated results to `/home/user/aggregated_output.json` as a JSON array of objects. 
The array must be sorted chronologically by `bucket`, and then alphabetically by `sensor_id`.

Example output format:
```json
[
  {
    "bucket": "2023-10-01T12:00:00Z",
    "sensor_id": "alpha_1",
    "mean_x": 10.5021,
    "mean_y": 2.1100
  },
  {
    "bucket": "2023-10-01T12:00:00Z",
    "sensor_id": "beta_2",
    "mean_x": 5.0000,
    "mean_y": 8.0000
  }
]
```

Write and execute your script to produce the final JSON file.