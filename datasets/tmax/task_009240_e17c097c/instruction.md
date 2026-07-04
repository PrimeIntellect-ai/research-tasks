You are acting as a security auditor for a web application. You have been provided with a dump of server logs, file manifests, and the application's static web directory. Your goal is to identify security vulnerabilities across HTTP headers, file integrity, file permissions, and Content Security Policy (CSP) enforcement. 

All files are located in `/home/user/audit`. You must use standard Bash tools to analyze the files and generate a final report.

Here are your specific tasks:

1. **HTTP Header and Cookie Inspection**: 
   Analyze the file `/home/user/audit/headers.log`. This file contains blocks of HTTP response headers mapped to endpoints (indicated by a line starting with `Endpoint: /path`).
   Find all endpoints that issue a `Set-Cookie` header but are missing the `HttpOnly` flag. 

2. **File Integrity Verification**:
   The directory `/home/user/audit/www/` contains the static files of the web app. The file `/home/user/audit/manifest.sha256` contains the expected SHA256 hashes of these files. 
   Verify the integrity of all files in the `www` directory against the manifest. Identify the exact files that fail the hash check (tampered files).

3. **Permission Checking**:
   For the files identified as tampered in step 2, check their Unix file permissions. Identify which of these tampered files are world-writable (e.g., others have write permission).

4. **Content Security Policy (CSP) Enforcement Analysis**:
   Inspect the contents of the tampered files. Attackers often inject malicious external scripts. Extract all external domains found in `<script src="https://[domain]/..."></script>` tags inside the tampered HTML files.

Create a final audit report at `/home/user/audit_report.txt` with exactly the following format (ensure lists are comma-separated without spaces, and sorted alphabetically):

```
[VULNERABLE_ENDPOINTS]
/api/v1/login,/api/v1/session

[TAMPERED_FILES]
/home/user/audit/www/index.html,/home/user/audit/www/js/app.js

[WORLD_WRITABLE_TAMPERED]
/home/user/audit/www/index.html

[MALICIOUS_DOMAINS]
evil.com,malware.net
```

Requirements:
- Ensure all paths in the report are absolute paths.
- Sort all comma-separated lists alphabetically.
- Do not add spaces after commas in the lists.
- If a section has no results, leave it blank (e.g., `[MALICIOUS_DOMAINS]\n\n`).