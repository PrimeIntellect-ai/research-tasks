You are an automation specialist managing a pipeline that ingests IoT sensor logs in JSON-Lines (JSONL) format. We are experiencing pipeline crashes due to malformed payloads and time-sync anomalies from compromised sensors.

You have two objectives:

**1. Fix the vendored JSON parser:**
We use a pure-bash JSON parser, `JSON.sh`, which is vendored at `/app/vendored/JSON.sh-0.4.1`. Recently, an erroneous patch was applied to it that breaks its handling of valid hex-based unicode escape sequences (e.g., `\uabcd`). It currently fails or drops letters, only allowing digits. 
Fix the regex or matching logic inside `/app/vendored/JSON.sh-0.4.1/JSON.sh` so that it correctly parses standard 4-character hex unicode escapes.

**2. Create a log anomaly detector:**
Write a Bash script at `/home/user/detect_anomalies.sh` that takes a single file path as an argument. The script must determine if the log file is "clean" or "evil" and exit with code `0` for clean files, and `1` for evil/anomalous files.

A log file is considered **evil** (anomalous) if it meets ANY of the following conditions:
- **Malformed Unicode:** It contains invalid unicode escape sequences (e.g., `\u` followed by non-hex characters, or less than 4 hex characters like `\u12Z4` or `\uABC`).
- **Timestamp Changepoint Anomaly:** The logs contain a `timestamp` field (in ISO8601 format, e.g., `2023-10-12T10:00:00Z`). Extract these timestamps. If any timestamp in the file is chronologically older than the immediately preceding log entry's timestamp (i.e., time jumps backward), it is a changepoint anomaly.

A log file is **clean** if all unicode escapes are valid hex, AND all timestamps are strictly monotonically increasing or equal.

Use your fixed `JSON.sh` (or tools like `grep`, `awk`, `date`) within your script to extract and analyze the data. Ensure your script is executable (`chmod +x`). 

Test your script against the provided datasets:
- `/app/corpus/clean/` contains valid logs.
- `/app/corpus/evil/` contains logs with bad escapes or retrograde timestamps.