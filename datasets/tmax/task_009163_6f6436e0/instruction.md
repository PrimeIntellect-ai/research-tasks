You are an automation specialist for an IoT platform. You are tasked with creating a robust, bash-only ETL data processing pipeline to handle a continuous stream of sensor logs. 

You have a large log file located at `/home/user/iot_sensors.log`. 

The expected format of valid log lines is strictly:
`[YYYY-MM-DD HH:MM:SS] [SENS-XXXX:TYPE] STATUS PAYLOAD`

Where:
- `YYYY-MM-DD HH:MM:SS` is a standard timestamp.
- `XXXX` is exactly a 4-digit number.
- `TYPE` is a fully uppercase alphabetical string (e.g., `TEMP`, `HUMID`, `PRESSURE`).
- `STATUS` is strictly either `OK` or `ERROR`.
- `PAYLOAD` is any remaining string on the line.

Your task is to create a bash script at `/home/user/process_logs.sh` that processes this file using standard Unix text-processing utilities (`grep`, `awk`, `sed`, `sort`, `uniq`, etc.). The script must take the log file path as its first argument and output two files:

1. `/home/user/error_summary.csv`
   - This file should contain an aggregated count of all valid `ERROR` logs, bucketed by Date, Hour, and Sensor Type.
   - Format: `YYYY-MM-DD,HH,TYPE,Count`
   - The file must be sorted chronologically, then by Type.
   - Example line: `2023-10-24,14,HUMID,15`

2. `/home/user/sampled_ok.log`
   - This file should contain a stratified 10% sample of all valid `OK` logs. 
   - Specifically, for *each* unique Sensor Type (e.g., `TEMP`, `HUMID`), you should extract the 1st, 11th, 21st, etc., `OK` log encountered in the file for that type.
   - The output format should perfectly match the original log lines.

Requirements:
- Filter out and ignore any malformed lines that do not strictly match the expected format described above.
- Ensure your script streams the data efficiently (do not try to load the entire file into a bash array).
- Execute your script against `/home/user/iot_sensors.log` so the two output files are generated.