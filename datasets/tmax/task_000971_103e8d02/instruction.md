I need your help building a log processing tool in C to investigate some suspicious system patterns. 

First, we received an automated voice briefing from the incident response team regarding the specific patterns we need to extract. The audio file is located at `/app/briefing.wav`. Please transcribe and listen to it carefully. It contains the exact parameters for the data transformation pipeline.

Based on the instructions in the audio, write a C program that reads server logs from `stdin` and writes the processed output to `stdout`.

The input log data will be provided line by line in a "wide" format:
`<timestamp> <user_id> <cpu_usage> <memory_usage> <disk_io> <network_io>`

Where:
- `timestamp` is an integer Unix timestamp.
- `user_id` is an alphanumeric string (max 16 characters).
- The four metrics (`cpu_usage`, `memory_usage`, `disk_io`, `network_io`) are floating-point numbers.

Your C program must:
1. Parse the text logs and extract the structured information.
2. Reshape the data from "wide" format to "long" format (yielding separate entries for `cpu`, `mem`, `disk`, and `net`).
3. Apply the time-based bucketing and windowed/rolling aggregation exactly as specified in the audio briefing.
4. Output the results to `stdout` in the format: 
`<bucket_timestamp> <user_id> <metric_name> <rolling_value>`
(Format the floating-point `rolling_value` to exactly 2 decimal places).

Compile your program to `/home/user/log_processor`. It must be highly robust and exactly match the required mathematical output, as it will be rigorously tested against millions of auto-generated fuzzing logs.