You are a compliance analyst tasked with generating a secure audit trail of suspicious login activity and preparing network defense rules based on these logs.

You have been provided with a raw log file located at `/home/user/logs/login_attempts.csv`. The file contains login attempt records with the following header:
`timestamp,ip_address,username,status`

Your task consists of the following steps:

1. **Data Processing & Analysis:**
   Write a Python script to analyze the CSV file. Identify all `ip_address`es that have strictly more than three (i.e., >= 4) `FAILED` login attempts.
   Extract all log rows (as a list of JSON objects, where keys match the CSV headers) corresponding to the `FAILED` attempts of these specific flagged IP addresses.

2. **Encryption:**
   Using the `cryptography` library in Python, encrypt the JSON-encoded list of flagged records using Fernet symmetric encryption. 
   You must use the pre-existing key located at `/home/user/keys/audit.key`. 
   Save the encrypted output to `/home/user/secure_archive/audit_report.enc`.

3. **File Permissions & Access Control:**
   To ensure the audit trail is secure, enforce the following permissions using standard Linux commands or Python:
   - The directory `/home/user/secure_archive/` must have `0700` permissions.
   - The encrypted report `/home/user/secure_archive/audit_report.enc` must have `0400` permissions.
   - The encryption key `/home/user/keys/audit.key` must have `0400` permissions.

4. **Network Policy Configuration:**
   Generate a shell script at `/home/user/network_policy/block_rules.sh` that will be run by system administrators to block the flagged IPs.
   The script should contain standard bash commands. For each flagged IP address (sorted in ascending string order), add an iptables rule to drop incoming traffic.
   The format for each rule must be exactly: `iptables -A INPUT -s <IP_ADDRESS> -j DROP`
   Ensure the generated shell script has executable permissions (`0744`).

**Environment Setup Notes:**
- You may need to install the `cryptography` package if it is not already available (`pip install cryptography`).
- Do not execute the `block_rules.sh` script, as you do not have root privileges. Just generate it with the correct contents and permissions.