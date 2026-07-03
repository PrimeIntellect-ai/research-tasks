You are acting as a security assistant to a network engineer. We are currently inspecting HTTP traffic logs and auditing the back-end Bash CGI scripts of an internal web server after a suspected compromise.

You need to perform a comprehensive security analysis spanning traffic inspection, cryptographic verification, Content Security Policy (CSP) enforcement analysis, and code auditing. You must use standard Bash tools (like `grep`, `awk`, `sha256sum`, `base64`, etc.) to complete this task.

Here is the environment you are working with:
- `/home/user/traffic_log.txt`: A custom-formatted log file containing recent HTTP responses captured by our firewall.
- `/home/user/known_malware_hashes.txt`: A text file containing known malicious SHA256 hashes (one per line).
- `/home/user/cgi-bin/`: A directory containing the server's backend Bash CGI scripts.

The `traffic_log.txt` file uses the following block format for each logged response:
```
===RESPONSE_ID: <ID>===
[Headers]
Header-Name: Header-Value
...
[Body_Base64]
<base64_encoded_response_body>
===END===
```

Your objective is to analyze these assets and generate a final report at `/home/user/security_report.txt` with the exact structure described below.

**Phase 1: Payload Hashing & Verification**
Extract the base64-encoded bodies from `traffic_log.txt`, decode them, and compute their SHA256 checksums. Compare these checksums against the hashes in `/home/user/known_malware_hashes.txt`.
Identify the `RESPONSE_ID` of any response containing a known malicious payload.

**Phase 2: CSP Enforcement Scanning**
Analyze the `[Headers]` section of each response in `traffic_log.txt`. A response is considered to have a "Weak/Missing CSP" if:
1. It is missing the `Content-Security-Policy` header entirely.
2. OR the `Content-Security-Policy` header contains the `unsafe-inline` directive.

**Phase 3: CWE Code Auditing**
Audit the Bash scripts located in `/home/user/cgi-bin/`. You need to map each script to one of the following Common Weakness Enumerations (CWE) based on its contents:
- `CWE-78` (OS Command Injection)
- `CWE-79` (Cross-Site Scripting)
- `CWE-22` (Path Traversal)

**Phase 4: Reporting**
Generate a file precisely at `/home/user/security_report.txt` formatted exactly as follows:

```
[Malicious Responses]
<RESPONSE_ID>:<SHA256_HASH>

[Weak CSP Responses]
<RESPONSE_ID>
<RESPONSE_ID>

[CGI Vulnerabilities]
<script_filename>:<CWE-ID>
<script_filename>:<CWE-ID>
```

**Constraints and Notes:**
- Sort the `RESPONSE_ID`s in ascending numerical order in the report.
- Sort the `script_filename`s in alphabetical order in the report.
- Ensure all decoded payloads are hashed directly (do not append extra newlines during decoding/hashing).
- The task is complete once `/home/user/security_report.txt` is perfectly formatted and populated with the correct findings.