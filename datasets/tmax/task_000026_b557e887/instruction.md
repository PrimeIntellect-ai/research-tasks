You are a localization engineer for a global software company. We are updating our internal Translation Memory (TM) engine. We receive a continuous stream of raw localization access and update logs from our external translation vendors, and we need to process these logs, compile a new TM pack using a proprietary compiler, and serve the results to our production infrastructure via a lightweight TCP service.

Your task is to write a Bash-based data processing pipeline and a TCP server to handle this workflow.

**Input Data:**
You are provided with a raw log file at `/home/user/l10n_logs.csv`. 
The format is: `Timestamp | IP_Address | User_Email | Action | Source_Text | Target_Text`
*   `Timestamp`: ISO 8601 format (e.g., `2023-10-04T14:32:01Z`).
*   `Action`: Can be `UPDATE`, `MISSING`, or `VIEW`.

**Processing Requirements:**
1.  **Data Masking (PII Anonymization):**
    Create a script to parse the CSV. Mask all IP addresses to `0.0.0.0` and mask the user part of all emails (before the `@`) to `***` (e.g., `john.doe@vendor.com` becomes `***@vendor.com`). Use regex for this.
2.  **Anomaly Detection (Time-based Bucketing):**
    Analyze the `MISSING` actions. Group the `MISSING` actions by hour (format `YYYY-MM-DDTHH`). Identify any "anomalous" hours where strictly more than 10 `MISSING` events occurred. Store these anomalous hours and their counts in a file called `/home/user/anomalies.txt` in the format: `YYYY-MM-DDTHH,Count`.
3.  **Hash-based Deduplication:**
    Filter the logs for `UPDATE` actions. We need to create a clean translation dictionary. For each unique `Source_Text`, compute its MD5 hash. If there are multiple `UPDATE` entries for the same `Source_Text`, keep only the one with the *most recent* timestamp. 
    Output a file `/home/user/clean_tm.csv` formatted as: `MD5_of_Source_Text,Target_Text` (no headers).
4.  **Compilation:**
    There is a proprietary, stripped binary located at `/app/tm_compiler`. You must pass the contents of `/home/user/clean_tm.csv` to its standard input. It will output a compiled binary translation pack to standard output. Save this output to `/home/user/pack.bin`.
5.  **Multi-Protocol Service:**
    Write a Bash script (using tools like `socat` or `nc`) that listens on TCP port `8888`. 
    *   When a client connects and sends the exact string `GET_ANOMALIES\n`, the server must reply with the exact contents of `/home/user/anomalies.txt` and close the connection.
    *   When a client sends `GET_PACK\n`, the server must reply with the raw binary contents of `/home/user/pack.bin` and close the connection.
    The server must run continuously to handle multiple sequential requests.

Do not use external databases; rely on Bash, coreutils, awk, sed, and standard Linux utilities. Ensure your TCP server is running in the background when you consider the task complete.