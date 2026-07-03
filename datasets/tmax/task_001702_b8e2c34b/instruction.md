You are a support engineer tasked with recovering diagnostic data from a crashed telemetry server. 

You have been provided with the following files:
1. `/app/sysadmin_voicemail.wav` - An audio recording left by the lead sysadmin detailing the crash context, the specific timezones involved, and the specific timeframe of interest. 
2. `/app/telemetry/telemetry.db` and `/app/telemetry/telemetry.db-wal` - A corrupted SQLite database and its Write-Ahead Log. A race condition caused a crash, leaving critical data uncommitted in the WAL.
3. `/app/logs/syslog.log` - A system log file containing JSON-encoded lines, some of which have base64-encoded payloads due to a serialization bug.

Your tasks are:
1. Transcribe or analyze `/app/sysadmin_voicemail.wav` to understand the timezone mismatch (the database was writing in a specific local time, while logs are in a different timezone) and the specific target time window.
2. Recover the uncommitted records from the SQLite WAL file.
3. Parse the `syslog.log`, decoding any base64 payloads to reveal the true log levels and tracebacks.
4. Align the timestamps from the database and the logs into a single, unified UTC timeline.
5. Extract all "CRITICAL" events that occurred within the target time window mentioned in the audio.
6. Write the results to `/home/user/critical_events.csv` with the headers exactly as: `timestamp_utc,source,message`. `source` should be either `db` or `syslog`. `timestamp_utc` must be in ISO 8601 format (e.g., `2023-10-25T05:30:00Z`).

You may use any language or standard Linux tools you prefer. Ensure your output is perfectly formatted, as it will be graded automatically.