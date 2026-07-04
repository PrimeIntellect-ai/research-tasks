You are an operations engineer triaging an incident. A daily data processing script, `/home/user/process_telemetry.py`, has been failing intermittently. The script processes telemetry logs and outputs a JSON file, but it crashes on specific days.

A previous run crashed in the middle of the night, leaving behind a raw memory dump of the frozen process state at `/home/user/process_memory.raw`. 

Your tasks are:
1. **Analyze the Memory Dump:** Inspect `/home/user/process_memory.raw` to extract the context of the crash. The application logs its crash context in a JSON-like string format containing the key `CRASH_CONTEXT:`. Find the `device_id` associated with this crash context and write just the device ID string to `/home/user/culprit_device.txt`.
2. **Diagnose and Fix the Bug:** The Python script fails due to a subtle timezone edge case when parsing the log format (specifically related to daylight saving time transitions). Fix `/home/user/process_telemetry.py` so that it handles ambiguous times gracefully. When a time is ambiguous (occurs twice due to a DST fallback), your fix must default to Standard Time (not Daylight Saving Time).
3. **Process the Data:** Once fixed, run the script against the provided log file `/home/user/data/telemetry.txt` and write the output to `/home/user/output.json` using the command: `python3 /home/user/process_telemetry.py /home/user/data/telemetry.txt /home/user/output.json`

Ensure the final `output.json` contains all processed records without throwing exceptions.