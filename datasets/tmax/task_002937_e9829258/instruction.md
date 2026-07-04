You are a log analyst at a high-security firm investigating a recent wave of stealthy lateral movement attacks. The attackers have been manipulating log files to hide their tracks, but they leave behind temporal anomalies and constraint violations.

Your task is to build an automated log detection script in Python that classifies log files as either clean or malicious. 

**System Setup:**
- You are provided with a black-box stripped binary at `/app/bin/temporal_decoder`. The engineering team lost the source code for this legacy tool. It takes a single obfuscated hex string as a command-line argument and prints the decoded standard UNIX epoch timestamp (integer) to standard output.
- Log files are provided in JSON Lines format (`.jsonl`). Each line is a JSON object representing a single event.

**Log Schema:**
Valid logs must contain exactly these four keys:
- `user_id` (string)
- `obfuscated_ts` (string, hex encoded)
- `event_type` (string)
- `ip_address` (string)

**Detection Rules:**
Your script must be located at `/home/user/filter.py`. It should take a single log file path as its first command-line argument (`sys.argv[1]`).

To evaluate a log file, your script must:
1. **Constraint Validation**: Ensure every JSON line has exactly the four required fields. If any line is missing a field or has extra fields, the file is immediately flagged as malicious.
2. **Normalization**: Use `/app/bin/temporal_decoder` to decode the `obfuscated_ts` for every event into a standard UNIX epoch integer.
3. **Time-based Bucketing**: Group the events into fixed 5-minute (300-second) tumbling windows, aligned to the UNIX epoch (i.e., a bucket starts at `timestamp // 300 * 300`).
4. **Anomaly Detection**: A log file is flagged as malicious if *any single 5-minute bucket* violates either of these conditions:
   - A single `user_id` originates from strictly more than 3 distinct `ip_address`es within that bucket.
   - The total count of `event_type` exactly equal to `"LOGIN_FAILED"` across *all* users in that bucket is strictly greater than 10.

**Output Specification:**
- If the log file violates ANY of the rules above, the script must print exactly `EVIL` to standard output and exit with status code `1`.
- If the log file passes all rules, the script must print exactly `CLEAN` to standard output and exit with status code `0`.

During your development, you can create your own test files to verify your script's behavior. We will automatically test your script against a hidden dataset of clean and malicious logs.