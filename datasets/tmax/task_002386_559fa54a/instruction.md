You are a support engineer investigating a bug in a nightly log processing pipeline. 

The pipeline uses a Python script located at `/home/user/process_logs.py` to parse custom log files. Currently, the script is reporting errors when processing the log file located at `/home/user/data/app.log`. 

The log file format is expected to be strictly:
`TIMESTAMP|LOG_LEVEL|JSON_PAYLOAD`

However, some recent user activities involve sending messages that contain the pipe character (`|`). The current parsing logic incorrectly splits the line when a pipe character appears inside the JSON payload, causing a `json.decoder.JSONDecodeError` or `IndexError`.

Your task:
1. Trace the intermediate state of the script to understand exactly which line is failing.
2. Repair the edge-case in the format parsing logic inside `/home/user/process_logs.py` so that it correctly extracts the JSON payload even if the payload contains pipe characters.
3. You are not allowed to modify the `/home/user/data/app.log` file.
4. Run the fixed script using the command: `python3 /home/user/process_logs.py /home/user/data/app.log`
5. The script will output a file named `/home/user/diagnostic_summary.json`. Ensure this file is generated successfully and reports zero errors.

The final state must have the corrected `process_logs.py` script and the generated `/home/user/diagnostic_summary.json` file.