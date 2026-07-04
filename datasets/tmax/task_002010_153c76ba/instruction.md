You are a compliance analyst generating secure audit trails. You have been provided with a raw authentication log file located at `/home/user/raw_auth.log`. This file contains sensitive information and records of a recent brute-force attack against our services. 

Your task is to process this log file using Python to generate two artifacts: a safely redacted audit log, and a shell script containing firewall rules to block the attackers.

The format of `/home/user/raw_auth.log` is exactly:
`[TIMESTAMP] | IP: <ip_address> | Port: <port> | User: <email> | Pass: <password> | Status: <Success/Failed>`

Write a Python script to do the following:

1. **Sensitive Data Redaction**: 
   Read `/home/user/raw_auth.log` and write the processed lines to `/home/user/audit_trail_redacted.log`.
   - The password must be completely replaced with `***`. (e.g., `Pass: secret123` becomes `Pass: ***`).
   - The domain of the user's email address must be masked with `***` (e.g., `User: admin@company.com` becomes `User: admin@***`).
   - All other fields and formatting must remain exactly as they are in the original log.

2. **Brute-Force Auditing and Firewall Policy Configuration**:
   Identify any IP address that has 3 or more `Status: Failed` attempts in the log.
   For each of these identified attacker IPs, write a command to a bash script located at `/home/user/block_ips.sh`.
   - The script should contain exactly one line per blocked IP in the following format: `iptables -A INPUT -s <IP> -j DROP`
   - Sort the commands in the script by the IP address in ascending alphabetical/string order.

Ensure both `/home/user/audit_trail_redacted.log` and `/home/user/block_ips.sh` are generated correctly before completing your turn.