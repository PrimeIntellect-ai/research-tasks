You are a data scientist taking over a legacy pipeline. We have telemetry data coming from multiple sensors in different formats, and we need to clean and reshape it. Furthermore, we have an old anomaly detection tool that was compiled as a binary, but we lost its source code. We need to rewrite the entire pipeline in Go.

Your objectives:

1. **Data Preparation**: Write a Go program at `/home/user/pipeline.go` that accepts a `prepare` subcommand:
   `go run pipeline.go prepare <input_csv> <input_json> <output_csv>`
   - The `<input_csv>` will be in wide format with columns: `timestamp,sensor_A,sensor_B`.
   - The `<input_json>` will be an array of objects: `[{"timestamp": 1600000000, "sensor_C": 10.5, "sensor_D": -3.2}, ...]`.
   - Your program must inner-join these datasets on `timestamp`, reshape the data from wide to long format, and write to `<output_csv>` with headers: `timestamp,sensor_id,value`.
   - The output CSV must be sorted chronologically by timestamp, and then alphabetically by `sensor_id`.

2. **Anomaly Detection**: Add a `detect` subcommand to your Go program:
   `go run pipeline.go detect <long_format_csv>`
   - This command must read a long-format CSV (like the one produced by `prepare`).
   - It must analyze the data to determine if there are any changepoint anomalies.
   - If the file is completely normal, it must print exactly `CLEAN` to standard output and exit with status `0`.
   - If the file contains any anomalies, it must print exactly `EVIL` to standard output and exit with status `1`.
   
3. **Reverse-Engineering the Oracle**:
   The exact definition of what constitutes an anomaly is locked inside our legacy detector. We have provided the stripped binary at `/app/telemetry_oracle`. 
   - You must figure out the mathematical rule it uses to classify a file as EVIL. (Hint: It relates to the absolute difference between consecutive chronological readings for the *same* sensor).
   - Once you deduce the threshold and logic, implement it natively in your Go `detect` subcommand.
   - **Do not** shell out to `/app/telemetry_oracle` in your final Go code. Your code will be tested in an environment where the oracle binary is removed.

A comprehensive automated test suite will evaluate your `detect` command against a large corpus of EVIL and CLEAN CSV files to verify it correctly mimics the legacy oracle.