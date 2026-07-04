As a data scientist, you are cleaning a batch of sensor data before ingestion. You have a raw CSV file at `/home/user/raw_sensors.csv` containing IoT temperature readings. The file has the following columns:
`timestamp,metadata,temp_loc1,temp_loc2,temp_loc3`

The data suffers from three issues:
1. It contains duplicate rows due to network retries.
2. It is in a "wide" format, but our database requires a "long" format.
3. The readings are too granular and need to be averaged over 1-hour intervals.

Write a Go program at `/home/user/clean.go` that performs the following data processing pipeline, and then run it to produce an output file at `/home/user/cleaned_sensors.csv`:

**Pipeline Steps:**
1. **Deduplication:** Read the raw CSV and remove duplicate rows. Two rows are considered identical if the SHA256 hash of their entire raw row string (excluding the newline character) is the same.
2. **Reshaping (Wide to Long):** Convert the three temperature columns (`temp_loc1`, `temp_loc2`, `temp_loc3`) into individual records. Each original row should yield three records with a `sensor_id` ("loc1", "loc2", or "loc3") and its corresponding `temp` value.
3. **Time-based Bucketing & Aggregation:** Parse the `timestamp` (RFC3339 format). Truncate the timestamp down to the start of the hour (e.g., `2023-10-01T10:45:00Z` becomes `2023-10-01T10:00:00Z`). Group the records by this 1-hour bucket and the `sensor_id`. Calculate the average temperature for each group.

**Output Constraints:**
Write the results to `/home/user/cleaned_sensors.csv` with the following headers:
`bucket,sensor_id,avg_temp`
- `bucket` should be formatted as RFC3339 (e.g., `2023-10-01T10:00:00Z`).
- `sensor_id` should be `loc1`, `loc2`, or `loc3`.
- `avg_temp` should be formatted to exactly 2 decimal places (e.g., `23.00`).
- The output CSV must be sorted chronologically by `bucket` ascending, and then alphabetically by `sensor_id` ascending.

Run your Go program to generate the final CSV.