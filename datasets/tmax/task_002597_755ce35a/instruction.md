You are a forensics analyst investigating a compromised Linux server. We suspect an attacker exploited a path traversal vulnerability in a file upload handler to overwrite critical application files.

Your investigation relies on the following evidence provided on the system:
1. **Application Files:** Located at `/home/user/app/`.
2. **Integrity Manifest:** A SHA256 checksum file of the known-good application state, located at `/home/user/app_manifest.sha256`.
3. **Web Server Logs:** Located at `/home/user/logs/access.log`.

Perform the following tasks:
1. **Cryptographic Checksum Verification:** Compare the files in `/home/user/app/` against `/home/user/app_manifest.sha256`. Identify exactly which files have been modified.
2. **Pattern Matching for Intrusion Detection:** Analyze `/home/user/logs/access.log` to identify the attacker's IP address. The attacker used path traversal sequences (e.g., `../`) in the URL or payload to target the specific files you identified in step 1.
3. **Content Security Policy Enforcement:** Analyze the compromised files. The attacker injected external JavaScript or data exfiltration URLs (look for domains that are not 'self'). Based on your analysis, define a strict Content Security Policy (CSP) `script-src` directive that allows scripts from `'self'` but would explicitly block the unauthorized external domains found in the payload.

Write your findings to a JSON file at `/home/user/report.json` with the exact following structure:
```json
{
  "compromised_files": [
    "/home/user/app/example1.ext",
    "/home/user/app/example2.ext"
  ],
  "attacker_ip": "X.X.X.X",
  "extracted_malicious_domains": [
    "malicious.example.com"
  ],
  "recommended_csp": "script-src 'self';"
}
```

Constraints:
- `compromised_files` must be a sorted array of absolute file paths.
- `extracted_malicious_domains` must be a sorted array of only the domain names (no HTTP/HTTPS scheme, no paths) found injected into the compromised files.
- `recommended_csp` must be exactly `"script-src 'self';"` as we want to enforce a strict same-origin policy for scripts.