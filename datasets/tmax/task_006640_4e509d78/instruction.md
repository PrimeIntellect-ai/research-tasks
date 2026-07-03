You are acting as a compliance and security analyst investigating a potential data breach on a Linux-based web server. 

An incident was reported where sensitive system files were accessed via a vulnerable Bash CGI script used for file downloading. Your task is to analyze the logs, identify the vulnerability, patch the script, verify file integrity of the system configuration, and generate an audit trail report.

All files are located in `/home/user/incident/`. 

**Phase 1: Log Parsing and Correlation**
You have two log files:
1. `/home/user/incident/logs/access.log` - Contains web server access logs. You must find the IP address that successfully exploited a Path Traversal attack (HTTP 200 response for an access attempt to a file outside the web directory).
2. `/home/user/incident/logs/auth.log` - Contains SSH authentication logs. Correlate the attacker's IP address to find which system user account they compromised to gain internal access later.

**Phase 2: Code Auditing and CWE Identification**
Review the script `/home/user/incident/cgi-bin/download.sh`. 
1. Identify the Common Weakness Enumeration (CWE) identifier for the vulnerability present in the script (format: `CWE-XXX`).
2. Patch the vulnerability directly in `/home/user/incident/cgi-bin/download.sh`. Ensure that the `file` parameter cannot contain directory traversal characters (`..` or `/`) and only allows alphanumeric characters, underscores, and periods. If invalid, the script should output `Invalid filename` and exit with code 1.

**Phase 3: File Integrity Verification**
The attacker may have altered configuration files. Compare the files in `/home/user/incident/backups/` against the files in `/home/user/incident/current/`.
Use `sha256sum` to identify which files have been modified (hashes do not match).

**Phase 4: Audit Trail Generation**
Write your findings to a strictly formatted JSON file at `/home/user/incident/audit_report.json`.
The JSON must have the following exact structure:

```json
{
  "attacker_ip": "<IP_ADDRESS>",
  "compromised_user": "<USERNAME>",
  "cwe_id": "<CWE-XXX>",
  "corrupted_files": [
    "filename1.ext",
    "filename2.ext"
  ]
}
```
*Note: Sort the `corrupted_files` array alphabetically.*

Use Bash to accomplish these tasks. Do not delete any original log files.