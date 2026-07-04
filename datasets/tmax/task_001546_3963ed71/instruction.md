You are acting as a security researcher investigating a suspicious Python worker process that recently crashed on this system. 

You have been provided with the following files in `/home/user/investigation/`:
1. `mem_dump.bin`: A raw memory dump taken just before the process terminated.
2. `logs/api.log`: Logs from the API service that the worker interacted with.
3. `logs/db.log`: Logs from the database service.

Your goal is to investigate the cause of the crash and extract Indicators of Compromise (IoCs). Specifically, you must write a Python script at `/home/user/investigate.py` that performs the following steps and outputs the results to `/home/user/report.json`:

1. **Memory Dump Analysis**: Parse `mem_dump.bin` to extract a suspicious domain name. The domain is known to end with `.malware.local`. You need to extract the exact domain name (e.g., `something.malware.local`) from the binary data.
2. **Log Timeline Reconstruction**: Merge the log entries from both `api.log` and `db.log`, and sort them chronologically to reconstruct the exact sequence of events.
3. **Misconfiguration Identification**: Identify the missing environment variable that triggered the crash. The logs will contain an `EnvironmentError` indicating which variable was not set.
4. **Report Generation**: Your script must generate a JSON file at `/home/user/report.json` with exactly the following schema:
```json
{
  "suspicious_domain": "<extracted_domain>",
  "missing_env_var": "<name_of_missing_variable>",
  "last_event_before_crash": "<the full log message text (without timestamp/level) of the event immediately preceding the CRASH event>"
}
```

Note: 
- The logs are formatted as `<ISO8601-Timestamp> <LEVEL> <Message>`.
- The "CRASH" event is logged with the `CRITICAL` level. 
- You do not need to fix the environment, only identify the missing variable.
- The `last_event_before_crash` should just be the message part (e.g., if the log is `2023-10-01T10:00:05Z ERROR EnvironmentError: FOO not set`, the message is `EnvironmentError: FOO not set`).

Ensure your script runs successfully and creates the required `/home/user/report.json` file.