You are a compliance analyst tasked with generating secure audit trails of potential malicious traffic. You have been provided with a file containing raw, Base64-encoded request logs. As part of a strict compliance framework, any processing of potentially malicious payloads must occur within an isolated environment, and the results must be evaluated against our strict Content Security Policy (CSP).

Your task is to create a two-part Bash-based analysis pipeline:

1. **Analysis Script (`/home/user/analyze.sh`):**
   Write a Bash script that reads `/home/user/raw_logs.txt`. 
   Each line in this file follows the format: `LogID:Base64EncodedPayload`.
   For each line, the script must:
   - Decode the Base64 payload.
   - Analyze the decoded payload for vulnerabilities:
     - Mark as `XSS` if the decoded payload contains the string `<script`, `javascript:`, or `onerror=`.
     - Mark as `SQLi` if the decoded payload contains the string `UNION SELECT` or `' OR 1=1`.
     - Mark as `None` if neither matches.
   - Enforce Content Security Policy (CSP): We have a strict CSP that disallows inline scripts and unsafe evals. If the threat is identified as `XSS`, our strict CSP would block it. Mark `CSP_Blocked` as `True` if it's an XSS threat, otherwise `False`.
   - Append the results to `/home/user/audit_trail.csv` in the exact format: `LogID,ThreatType,CSP_Blocked,DecodedPayload` (Note: if the decoded payload contains commas, do not worry about escaping them for this simple challenge, just output the raw decoded string).

2. **Isolation Runner (`/home/user/run_isolation.sh`):**
   To satisfy compliance requirements regarding the handling of unverified payloads, the analysis must be run in an isolated network and user namespace. 
   Write a Bash script at `/home/user/run_isolation.sh` that executes your `analyze.sh` script using the `unshare` command to create a new, isolated user and network namespace (e.g., mapping to the root user inside the namespace and disabling networking).

Requirements:
- Ensure both scripts are executable.
- Run `/home/user/run_isolation.sh` so that the final `/home/user/audit_trail.csv` is generated.
- The `audit_trail.csv` must NOT contain a header row.
- The base64 payloads may decode to strings with spaces.

Example output row in `audit_trail.csv`:
`LOG-001,XSS,True,<script>alert(1)</script>`