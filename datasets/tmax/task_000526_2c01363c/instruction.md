You are acting as a security auditor. You have been provided with an archive of data from a potentially compromised server. Your task is to analyze this data, remediate insecure configurations, redact sensitive information from the logs, and generate a firewall rule set to block attackers.

All your work must take place within the `/home/user/audit_task` directory.

The initial state of `/home/user/audit_task/raw_data` contains:
1. `auth_logs.jsonl`: A JSON Lines file containing authentication events.
2. `sshd_config.insecure`: The server's current SSH daemon configuration file.
3. `bin/`: A directory containing a few critical system binaries (simulated as text files for this exercise).
4. `checksums.sha256`: A standard SHA256 checksum file for the contents of the `bin/` directory.

Your objectives are to write scripts (preferably in Python) to perform the following tasks and output the results to `/home/user/audit_task/results/` (you will need to create this directory):

**Objective 1: Sensitive Data Redaction & Log Analysis**
Read `auth_logs.jsonl`. Many entries incorrectly logged plain-text passwords. 
- You must create `/home/user/audit_task/results/redacted_logs.jsonl`.
- The output must be identical to the input, EXCEPT that any JSON key named exactly `"password"` or `"secret_token"` must have its value replaced with the exact string `"[REDACTED]"`.
- While processing the logs, count the number of times each IP address is associated with the `"event_type": "failed_login"`.

**Objective 2: Firewall Policy Configuration**
Identify any IP address that has strictly MORE than 3 `"failed_login"` events in the logs.
- Create `/home/user/audit_task/results/firewall_rules.txt`.
- For each identified malicious IP address, add exactly one line to this file in the following format:
  `iptables -A INPUT -s <IP_ADDRESS> -j DROP`
- Sort the lines in ascending alphabetical order by IP address.

**Objective 3: SSH Hardening**
Read the `sshd_config.insecure` file.
- Create a hardened version at `/home/user/audit_task/results/sshd_config.secure`.
- The new file must be identical to the original, with the following modifications:
  - Find the line configuring `PermitRootLogin` and change its value to `no` (e.g., `PermitRootLogin no`). If it is commented out, uncomment it.
  - Find the line configuring `PasswordAuthentication` and change its value to `no`. If it is commented out, uncomment it.

**Objective 4: Cryptographic Integrity Check**
Verify the SHA256 checksums of the files in `/home/user/audit_task/raw_data/bin/` against `/home/user/audit_task/raw_data/checksums.sha256`.
- One file has been modified and will NOT match its checksum. Identify this compromised file.

**Objective 5: Final Audit Summary**
Create a final JSON report at `/home/user/audit_task/results/audit_summary.json` containing exactly the following structure:
```json
{
  "compromised_file": "name_of_the_modified_file_inside_bin_dir",
  "malicious_ips_count": <integer_number_of_ips_blocked>
}
```

Ensure all your output files exactly match the requested names, paths, and formats.