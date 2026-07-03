You are a Compliance Security Analyst tasked with generating an audit trail for a recent security incident. We have isolated a web application source file and its associated reverse-proxy event logs. 

Your objective is to write a Python script (`/home/user/analyze.py`) that analyzes the source code and logs to identify successful exploits, verify HTTP header compliance, and generate remediation firewall rules.

Here are the files provided to you:
1. `/home/user/app.py`: A Python web application.
2. `/home/user/security_events.log`: A JSON Lines (JSONL) log file where each line contains request and response data (e.g., timestamp, source_ip, method, path, status_code, response_headers).

**Step-by-Step Requirements:**

1. **Vulnerability Analysis:** Inspect `/home/user/app.py` to identify which API endpoint path (e.g., `/api/vX/something`) is vulnerable to SQL Injection due to raw string formatting/concatenation in the database query.
2. **Log Parsing & Correlation:** Parse `/home/user/security_events.log`. Find all log entries where:
   - The request targets the vulnerable endpoint identified in Step 1.
   - The request path/query string contains a basic SQL injection payload (specifically, check if the URL-decoded path contains a single quote `'` followed by either `UNION`, `SELECT`, or `--` case-insensitively).
   - The response `status_code` is `200` (indicating the query executed successfully).
3. **HTTP Header Inspection:** For the matched malicious requests, inspect the `response_headers` dictionary. A response is considered non-compliant if it is missing BOTH `Content-Security-Policy` AND `Strict-Transport-Security` headers.
4. **Audit Trail Generation:** Output the findings to a CSV file at `/home/user/audit_trail.csv` with the exact following header row:
   `Timestamp,Attacker_IP,Vulnerable_Endpoint,Missing_Security_Headers`
   - `Missing_Security_Headers` should be `True` if non-compliant according to Step 3, otherwise `False`.
   - Sort the CSV rows chronologically by Timestamp.
5. **Firewall Policy Configuration:** Generate a bash script at `/home/user/block_ips.sh` that contains `iptables` rules to drop all incoming traffic from the identified attacker IP addresses.
   - Use the format: `iptables -A INPUT -s <IP> -j DROP`
   - Include one command per unique IP, sorted alphanumerically.
   - Make the script executable (`chmod +x`).

Do not include any raw setup code or libraries that require external network access to install; standard Python libraries (like `json`, `csv`, `urllib.parse`, `re`) are sufficient. Execute your script to generate the required output files before completing the task.