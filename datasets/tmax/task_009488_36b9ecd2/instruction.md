You are acting as a data scientist cleaning up a large, messy sensor dataset. You have a server log file located at `/home/user/sensor_data.log`. The file is too large to load entirely into memory, so you must process it as a stream.

The log file is pipe-separated (`|`) and has the following format (including potential leading/trailing spaces around values):
`TIMESTAMP | SENSOR_ID | REGION | TEMPERATURE | HUMIDITY`

Example row:
`2023-10-12T08:00:00Z | S-992 | NA-WEST | 85.2 | 40.1`

Your task is to write and execute a Bash shell script that streams this file, extracts relevant features, and generates an alert payload for specific anomalous readings. 

Specifically, you must:
1. Extract rows where the `REGION` is exactly `EU-CENTRAL` (ignoring surrounding whitespace) AND the `TEMPERATURE` is strictly greater than `90.0`.
2. For each matching row, generate a single line in a new file `/home/user/alerts.jsonl` using the following exact JSON template:
`{"alert_type": "HighTemp", "timestamp": "<TIMESTAMP>", "sensor": "<SENSOR_ID>", "reading": <TEMPERATURE>}`

Replace `<TIMESTAMP>`, `<SENSOR_ID>`, and `<TEMPERATURE>` with the exact, trimmed values extracted from the row.

Requirements:
- Ensure your script correctly handles whitespace padding around the pipe delimiters.
- The output file must be written to `/home/user/alerts.jsonl`.
- Write your processing logic into a script at `/home/user/process.sh` and run it to produce the output. Use standard Unix utilities (e.g., `awk`, `sed`, `bash`) to ensure memory-efficient streaming.