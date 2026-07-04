You are a forensics analyst recovering evidence from a compromised Linux web server. The web application is located in `/home/user/webapp`. You suspect the attacker has modified source files, injected malicious traffic, and weakened the Content Security Policy (CSP) to facilitate cross-site scripting (XSS) and data exfiltration.

Your objective is to analyze the compromised state, identify the attack vectors, and prepare a forensic report using Python. 

Please perform the following steps:

1. **File Integrity Verification**: 
   A list of the original, known-good SHA-256 hashes for the web application is stored in `/home/user/backup_hashes.txt` (format: `<sha256_hash>  <filename>`). 
   Write a Python script to hash the current files in the `/home/user/webapp/` directory. Compare them against the backup hashes. Any file that is missing from the backup list, or whose hash does not match, is considered an "integrity violation".

2. **Pattern Matching for Intrusion Detection**:
   The web access logs are stored in `/home/user/logs/access.log`. The attacker attempted directory traversal attacks. Use Python to parse this log file and extract all unique source IP addresses that made requests containing the directory traversal sequences `../` or `%2e%2e%2f` (case-insensitive) in the request URL.

3. **Content Security Policy Enforcement**:
   The application's headers are configured in `/home/user/webapp/config.json`. The attacker has weakened the `Content-Security-Policy` header by adding `'unsafe-inline'` and an unauthorized external domain (`http://evil.com`) to the `script-src` directive.
   Analyze the JSON file, remove `'unsafe-inline'` and `http://evil.com` from the `Content-Security-Policy` string, and format the fixed CSP string so that any extraneous spaces are removed. Do not modify the original `config.json` file.

4. **Forensic Report Generation**:
   Compile your findings into a strictly formatted JSON file at `/home/user/forensic_report.json`. The JSON must have the following exact structure:

```json
{
  "integrity_violations": ["<filename1>", "<filename2>"],
  "attacker_ips": ["<ip1>", "<ip2>"],
  "fixed_csp": "<corrected_csp_string>"
}
```

**Constraints & Notes:**
- The `integrity_violations` list must contain just the filenames (e.g., `"utils.py"`), sorted alphabetically.
- The `attacker_ips` list must contain unique IP addresses sorted in ascending alphabetical order.
- The `fixed_csp` string should be the corrected policy, for example: `"default-src 'self'; script-src 'self';"`.
- All operations should be performed in `/home/user`.