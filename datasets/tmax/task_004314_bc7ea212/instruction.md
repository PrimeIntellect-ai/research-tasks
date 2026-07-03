You are tasked with fixing a broken configuration audit pipeline. An upstream ETL job has been retrying failed batches, resulting in duplicate configuration change records in our raw logs. Furthermore, we need to implement an anomaly detection gate to flag suspicious bursts of configuration changes or unexpected version jumps.

Write a C program that reads a raw log file, cleans and deduplicates the records, applies a mathematical changepoint/anomaly detection logic, and writes the output to a normalized CSV file.

**Inputs:**
The raw log file is located at `/home/user/raw_audit_logs.txt`.
Each line is either corrupted (to be discarded) or follows this exact format:
`[YYYY-MM-DD HH:MM:SS] IP=<ip_address> USER=<username> ACTION=<action_name> CONFIG_V=<integer> RETRY=<0_or_1>`

**Requirements:**

1. **Regex Parsing & Cleaning:**
   * Write a C program located at `/home/user/audit_processor.c`.
   * Use POSIX regex (`regex.h`) to parse the lines. Discard any lines that do not strictly match the format above.

2. **Deduplication:**
   * The ETL retry bug causes duplicate events. If a parsed log entry has the exact same `USER`, `ACTION`, and `CONFIG_V` as the *immediately preceding* valid parsed log entry, and occurs within 10 seconds of that preceding entry, it is a duplicate.
   * Discard the duplicate. Keep only the first occurrence.

3. **Anomaly Detection (Mathematical / State Tracking):**
   * Keep track of the configuration changes as you process them chronologically.
   * **Rule 1 (Rate Anomaly):** If a user performs a valid, non-duplicate action and they have already performed 3 or more valid actions in the preceding 60 seconds (i.e., this is the 4th action within a <= 60 second sliding window for that specific user), flag this new action with `ANOMALY_RATE`.
   * **Rule 2 (Version Anomaly):** Keep track of the highest `CONFIG_V` seen *globally* so far. If a new valid record has a `CONFIG_V` that is more than 50 greater than the previously seen maximum global `CONFIG_V`, flag it with `ANOMALY_VERSION`. (The first valid record processed never gets `ANOMALY_VERSION`).

4. **Output Generation:**
   * Output the valid, deduplicated records to `/home/user/processed_audit.csv`.
   * Format: `UnixEpochTime,Username,Action,ConfigVersion,Flags`
   * `UnixEpochTime` must be a standard integer timestamp (assume UTC for parsing the log's time).
   * `Flags` must be one of: `NONE`, `ANOMALY_RATE`, `ANOMALY_VERSION`, or `ANOMALY_RATE|ANOMALY_VERSION` (if both apply).

**Execution:**
Compile your C program to `/home/user/audit_processor` (using `gcc -o /home/user/audit_processor /home/user/audit_processor.c -Wall`). Then run the program so that `/home/user/processed_audit.csv` is produced.