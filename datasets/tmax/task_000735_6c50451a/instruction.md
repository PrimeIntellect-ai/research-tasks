You are acting as a security auditor for a small web application. The application files are located in `/home/user/webapp/`. Recently, there was a suspected breach, and you need to perform an audit to check file permissions, verify file integrity, and look for injected vulnerabilities.

You have been provided with an original hash manifest located at `/home/user/manifest.txt`. This file contains the expected SHA-256 hashes of all the files in the `webapp` directory in the format:
`filename expected_sha256_hex`

Your objective is to analyze the current state of the application and generate a JSON report.

Perform the following tasks:
1. **Permissions Audit**: Identify any files within `/home/user/webapp/` that are world-writable (i.e., the "others" class has write permissions).
2. **Integrity Audit**: Calculate the SHA-256 hash of each file currently in `/home/user/webapp/` and compare it against the expected hash in `/home/user/manifest.txt`. Identify any files whose checksums do not match.
3. **Vulnerability Analysis**: Analyze the files that have **mismatched checksums**. Look for obvious signs of injected vulnerabilities:
   - Identify any files containing an injected Cross-Site Scripting (XSS) payload.
   - Identify any Python files containing an injected Command Injection vulnerability (e.g., using unsanitized user input in `os.system`, `subprocess`, or `eval`).

Write your findings to a file exactly at `/home/user/audit_report.json`. The file must be valid JSON and strictly follow this schema:

```json
{
  "world_writable_files": [
    "/home/user/webapp/example.html"
  ],
  "checksum_mismatches": [
    "/home/user/webapp/example.html",
    "/home/user/webapp/script.py"
  ],
  "xss_vulnerable_files": [
    "/home/user/webapp/example.html"
  ],
  "command_injection_files": [
    "/home/user/webapp/script.py"
  ]
}
```
*Note: Use absolute paths (e.g., `/home/user/webapp/filename.ext`) for all file entries in the JSON arrays. If an array has no matching files, leave it empty `[]`.*