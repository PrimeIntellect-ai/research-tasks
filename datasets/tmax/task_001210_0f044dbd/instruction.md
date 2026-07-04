As a DevSecOps engineer, you need to enforce a new "Policy as Code" standard for application logging. We recently discovered that our application logs contain sensitive customer data, leaked password hashes, and traces of untreated intrusion attempts.

Your task is to write a Python script that analyzes and cleans the raw application logs.

You are provided with two files:
1. `/home/user/raw_logs.txt`: The raw application logs.
   Format: `[TIMESTAMP] [IP] [LEVEL] MESSAGE`
2. `/home/user/wordlist.txt`: A short dictionary of common passwords.

Write a Python script at `/home/user/policy_enforcer.py` that reads `/home/user/raw_logs.txt` and performs the following three tasks:

**1. Data Redaction**
Find any Credit Card numbers in the logs and replace them entirely with the exact string `[REDACTED]`.
Credit card numbers are formatted exactly as four groups of four digits separated by hyphens (e.g., `1234-5678-9012-3456`). Save the completely processed (redacted) log file to `/home/user/redacted_logs.txt`. Maintain the exact original line order and formatting, just with the CC numbers swapped out.

**2. Intrusion Detection**
Identify any IP addresses that have made 3 or more malicious requests. A request is considered malicious if the log line (specifically the MESSAGE part) contains either of the following exact substrings (case-insensitive):
- `<script>`
- `' or '1'='1`

**3. Password Cracking / Auditing**
Some logs with the `[DEBUG]` level have accidentally leaked user password hashes in the format `Auth failed: hash=<MD5_HASH>`.
Extract these MD5 hashes and use the `/home/user/wordlist.txt` file to crack them. Keep a mapping of any successfully cracked hashes to their plaintext values.

**Outputs required:**
Run your Python script to generate the following outputs:

1. `/home/user/redacted_logs.txt`: The full log file with credit card numbers redacted.
2. `/home/user/security_report.json`: A JSON file containing the results of your intrusion detection and password cracking. It must exactly match this structure:
```json
{
  "blocked_ips": [
    "10.0.0.5",
    "..."
  ],
  "weak_passwords": {
    "hash1_string": "cracked_plaintext1",
    "hash2_string": "cracked_plaintext2"
  }
}
```
*Note: The `blocked_ips` list should be sorted alphabetically. Only include hashes in `weak_passwords` that were successfully cracked using the provided wordlist.*