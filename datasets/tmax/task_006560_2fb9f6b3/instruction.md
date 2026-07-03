You are an automation specialist creating an edge-data processing pipeline. You need to write a Go program that acts as a pipeline filter for IoT sensor data. 

There is an input file at `/home/user/input.jsonl` containing JSON Lines data from various sensors. You must write a Go program at `/home/user/pipeline.go` that reads from `stdin`, processes the data, writes the transformed JSON Lines to `stdout`, and writes pipeline statistics to `stderr`.

Implement the following processing rules in your Go program:
1. **Validation / Cleaning**: Drop any JSON record that does not have a `timestamp` field or where the `timestamp` is an empty string.
2. **Deduplication**: Keep track of the `event_id` field. If you encounter an `event_id` you have already seen in the stream, drop the record. Keep only the first occurrence.
3. **Normalization**: The input contains a nested object `sensor_data` with a key `temperature_f` (Fahrenheit float64). Convert this to Celsius using the formula `C = (F - 32) * 5 / 9`. Round the result to exactly 2 decimal places. Replace the `temperature_f` key with `temperature_c` containing the new value.
4. **Feature Extraction**: The input has a `user_agent` string like `"SensorX-9000/1.0"`. Extract the device model (everything before the first `/`). Add this extracted string as a new top-level field `device_model` in the JSON, and remove the original `user_agent` field entirely.
5. **Pipeline Logging**: After processing all input, print exactly one JSON line to `stderr` with the following structure showing pipeline execution stats:
   `{"total_read": 0, "dropped_invalid": 0, "dropped_duplicates": 0, "total_output": 0}`

Once your script is ready, run it using the standard Linux pipe to process the data:
`cat /home/user/input.jsonl | go run /home/user/pipeline.go > /home/user/output.jsonl 2> /home/user/stats.json`

Requirements:
- Only use standard Go libraries (no external packages like `go-yaml` or `tidwall/gjson`).
- Ensure the JSON fields precisely match the requested output format.