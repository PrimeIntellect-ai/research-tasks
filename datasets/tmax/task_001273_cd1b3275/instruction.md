You are a log analyst investigating anomalous patterns in a remote server farm's telemetry. We have historical telemetry data, but a recent network outage meant some logs were only transmitted via an emergency automated radio broadcast. 

Your task involves recovering this data, merging it with historical logs, and building a robust data processing pipeline to normalize the telemetry for downstream analysis.

**Step 1: Audio Recovery**
We have captured the emergency automated radio broadcast in an audio file located at `/app/intercept.wav`. The broadcast contains a synthesized voice reading out missing log entries. 
Extract the spoken log entries. The voice speaks in the format: "Time [timestamp], [SensorName] [value], [SensorName] [value]".

**Step 2: Data Merging & Processing Script**
You must write an executable script at `/home/user/process_telemetry` (you may use Python, Node.js, bash, etc., but it must be executable directly from the command line). This script must read wide-format JSONL data from `stdin` and output a normalized, interpolated CSV to `stdout`.

The input JSONL will have lines formatted like:
`{"time": 1600000005, "sensors": {"alpha": 12.4, "beta": 8.1}}`
*(Note: some lines might have missing sensors, or sensors might report at different times).*

Your script must perform the following pipeline:
1. **Wide-Long Format Reshaping:** Flatten the nested wide-format JSONL into a long format of `(sensor, time, value)`.
2. **Sorting and Grouping:** Group the records by `sensor` name, and sort each group strictly by `time` (ascending). If there are duplicate timestamps for the same sensor, take the average of the values.
3. **Resampling and Gap-filling:** For each sensor independently, determine its minimum and maximum timestamp. Create a continuous time series at exactly 1-second intervals from its `min_time` to its `max_time`. Fill any missing timestamps using exact mathematical linear interpolation between the nearest surrounding known points.
4. **Formatting:** Output the final data as a CSV to `stdout` with the header `sensor,time,value`. Sort the final CSV by `sensor` alphabetically, and then by `time` ascending. Round the `value` to exactly 4 decimal places (e.g., `12.4000`).

**Step 3: Final Analysis**
We have a historical log file at `/app/historical_logs.jsonl`.
Combine the extracted data from the audio intercept (formatting it as JSONL) with the historical logs. Pipe this combined dataset into your `/home/user/process_telemetry` script and save the output to `/home/user/final_analysis.csv`.

Ensure your script is robust! An automated testing suite will run your script against thousands of random telemetry streams to verify mathematical equivalence to our reference processing engine.