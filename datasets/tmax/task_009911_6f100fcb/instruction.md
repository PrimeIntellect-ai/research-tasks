You are a log analyst investigating application performance. You have been given a messy log file at `/home/user/raw_app.log`. An earlier pipeline failed to analyze this file correctly because some log entries contain multi-line stack traces (embedded newlines) which broke the CSV parser.

Your objective is to build a robust Bash pipeline (written in a script at `/home/user/process_logs.sh`) that processes these logs, handles the multi-line anomalies, anonymizes PII, calculates rolling aggregates, and flags performance anomalies.

The raw log entries look like this:
`[YYYY-MM-DD HH:MM:SS] IP=<ip_address> STATUS=<code> TIME=<ms> MSG=<message...>`
Sometimes, `<message...>` spans multiple lines before the next `[` starts a new log entry.

Your script must perform the following tasks:
1. **Extraction & Multi-line Handling:** Extract the Timestamp, IP, STATUS, and TIME. Ignore the MSG entirely. Treat any line that does not start with `[` as a continuation of the previous log entry's MSG and drop it.
2. **Data Masking:** Anonymize all extracted IP addresses by replacing the last octet with `xxx` (e.g., `192.168.1.55` becomes `192.168.1.xxx`).
3. **Windowed Aggregation:** Group the logs by minute (e.g., `YYYY-MM-DD HH:MM`). Calculate the average response `TIME` for each minute. Round the average down to the nearest integer.
4. **Anomaly Detection:** Identify anomalous minutes where the average `TIME` is strictly greater than 500 ms.
5. **Output 1 - Anomalies:** Create a CSV file at `/home/user/anomalies.csv` listing the anomalous minutes. It must have a header and be formatted exactly as:
   `Minute,AvgTime`
   *(Example: `2023-10-24 10:01,700`)*
6. **Output 2 - Stratified Samples:** Create a log file at `/home/user/anomalous_samples.log` containing all extracted log events that occurred *only* during the anomalous minutes detected in step 4. Format each line as a comma-separated list:
   `YYYY-MM-DD HH:MM:SS,MaskedIP,STATUS,TIME`
   *(Example: `2023-10-24 10:01:15,10.0.0.xxx,500,800`)*

Constraints:
- Your script `/home/user/process_logs.sh` must be written in Bash (using tools like `awk`, `sed`, `grep`, `sort`, etc.).
- Ensure your script has executable permissions and can be run to produce the outputs.
- Do not use Python, Perl, or Ruby for the data processing pipeline; stick strictly to Bash and standard GNU utilities.