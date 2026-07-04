You are acting as a data engineer maintaining an ETL pipeline. We have a stream of sensor data saved as a JSON-lines file at `/home/user/sensor_stream.jsonl`. 

Unfortunately, the upstream system occasionally produces malformed unicode escape sequences in the metadata field (e.g., `\uZZZZ`), which causes standard JSON parsers to throw exceptions. 

Your task is to write and execute a Python script at `/home/user/process_stream.py` that processes this file line by line and implements the following requirements:

1. **Error Handling & Parsing:** Attempt to parse each line as JSON. If a line fails to parse due to invalid JSON (such as a bad unicode escape sequence), catch the exception and do not crash.
2. **Rolling Statistics:** For valid records, extract the `temperature` (a float). Maintain a rolling average of the `temperature` over the last 3 **valid** readings. If fewer than 3 valid readings have been processed so far, compute the average of the available valid readings.
3. **Template-Based Logging:** Write a pipeline log to `/home/user/pipeline_output.txt`. For every line in the input file (starting at line 1), append one of the following exact templates to the log file:
   - For valid JSON lines: `SUCCESS: Sensor {sensor_id} processed. Rolling avg: {avg:.2f}`
   - For invalid JSON lines: `ERROR: Line {line_num} failed validation`

Requirements:
- Ensure the average is formatted to exactly 2 decimal places.
- The input file is `/home/user/sensor_stream.jsonl`.
- The output must be written to `/home/user/pipeline_output.txt`.
- Do not use any external dependencies outside the Python standard library.

Please write the script, run it, and ensure the log file is generated successfully.