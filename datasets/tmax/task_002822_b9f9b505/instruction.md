You are a log analyst investigating application crashes. A recent incident corrupted our JSON-lines log file, inserting invalid unicode escape sequences that break our standard JSON parsers. Furthermore, the logs contain raw IP addresses that must be anonymized before sharing with the development team. 

Your task is to write a Bash script at `/home/user/process.sh` that processes the file `/home/user/corrupt_logs.jsonl` and outputs a cleaned, anonymized, and deduplicated file at `/home/user/clean_logs.jsonl`.

Your script must perform the following pipeline:
1. **Parallel Processing:** Process the log lines in parallel (e.g., using `xargs -P`, `parallel`, or background bash processes). 
2. **Normalization (Fix Invalid Unicode):** Find any literal instances of `\u` followed by exactly 4 characters where AT LEAST ONE of those 4 characters is NOT a valid hexadecimal digit (`0-9`, `a-f`, `A-F`). Replace the entire invalid 6-character sequence (e.g., `\uXYZW`) with `\uFFFD`. Leave valid unicode sequences intact.
3. **Data Masking (Anonymization):** The logs contain an `"ip"` field (IPv4). Mask the final octet of every IP address with `XXX` (e.g., `192.168.1.100` becomes `192.168.1.XXX`).
4. **Hash-Based Deduplication:** Extract the `"message"` field from each log line. Calculate the SHA-256 hash of this message string. If multiple log entries have the same message hash, keep only the *first* one encountered (order in the final file does not matter, as long as there is only one entry per unique message).
5. **Output Format:** The final `/home/user/clean_logs.jsonl` must be a valid JSON-lines file where each line contains the updated JSON object. Add a new field `"msg_hash"` containing the computed SHA-256 hash.

Example Input Line:
`{"id": "101", "ip": "203.0.113.42", "message": "Failed to load component \uXYZW"}`

Expected Output Line:
`{"id": "101", "ip": "203.0.113.XXX", "message": "Failed to load component \uFFFD", "msg_hash": "2172775f0f353a27db..."}`

The script should be executable and can be run as `/home/user/process.sh`. Ensure `jq`, `sed`, `awk`, or any standard text processing tools are used safely.