You are a data analyst tasked with processing a telemetry dataset from IoT sensors using Go. 

You have a CSV file located at `/home/user/telemetry.csv` containing sensor readings. Since this file format is representative of massive datasets, your solution must process the file as a stream (reading row by row) rather than loading all records into memory at once.

The CSV has the following headers:
`timestamp,device_id,temperature,humidity`

You need to write a Go program at `/home/user/processor.go` that streams the CSV and produces a JSON-Lines file at `/home/user/output.jsonl`.

For each `device_id`, your program must:
1. **Compute a Rolling Average:** Calculate the moving average of the `temperature` over the last 3 records (including the current record) for that specific `device_id`. If fewer than 3 records have been seen for a device, calculate the average using the available records.
2. **Compute Distance:** Calculate the Euclidean distance of the current `(temperature, humidity)` from an ideal baseline point of `(20.0, 50.0)`.
3. **Stratified Sampling:** To reduce output size, only output every 2nd record observed for each `device_id` (i.e., the 2nd, 4th, 6th... records for device A, the 2nd, 4th... for device B).

**Output Format:**
The output must be a valid JSON-Lines file. Each emitted line should be a JSON object with these exact keys:
- `"device_id"`: (string)
- `"timestamp"`: (string)
- `"temp_avg"`: (string) The moving average, formatted to exactly 2 decimal places (e.g., `"21.00"`).
- `"distance"`: (string) The Euclidean distance, formatted to exactly 2 decimal places (e.g., `"2.24"`).

Compile and run your Go program to generate `/home/user/output.jsonl`.