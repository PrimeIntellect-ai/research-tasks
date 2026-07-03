You are acting as a security auditor. We need to perform a local security audit on a deployed application directory located at `/home/user/app_audit`. 

Your objective is to identify potential privilege escalation vectors (specifically, world-writable files), generate cryptographic hashes of these vulnerable files to establish a baseline, and audit the application's network and content security policies.

Please perform the following actions:
1. Scan the directory `/home/user/app_audit` recursively to find all files that are world-writable (others have write permission).
2. Calculate the SHA256 checksum for each world-writable file found.
3. The application has a configuration file located at `/home/user/app_audit/network_policy.json`. This file contains firewall rules and Content Security Policy (CSP) headers. Parse this JSON file.
4. Extract all CSP strings from the `csp` array in the JSON file that are insecure. For this audit, a CSP is considered insecure if it does NOT contain the directive `default-src`.
5. Compile your findings into a JSON report located at `/home/user/audit_report.json`. 

You may use Bash commands or write a Python script to accomplish this.

The output file `/home/user/audit_report.json` must exactly match the following format:
```json
{
  "vulnerable_files": {
    "/home/user/app_audit/path/to/file1.py": "<sha256_hash_here>",
    "/home/user/app_audit/path/to/file2.txt": "<sha256_hash_here>"
  },
  "insecure_csp": [
    "<insecure_csp_string_1>",
    "<insecure_csp_string_2>"
  ]
}
```
Ensure the JSON is properly formatted.