You are acting as a compliance analyst generating an automated audit trail for a recent security incident. We have a set of custom application logs, and we suspect an attacker was probing our authentication endpoints with injection attacks.

Your task is to create a Rust utility that parses these logs, correlates them with known attack signatures, and automatically tests our staging authentication service to see if it is vulnerable to the extracted payloads.

Here are the specific details:

1. **Log Location & Format:**
   The log file is located at `/home/user/auth.log`.
   Each line contains a failed login attempt in the following format:
   `[TIMESTAMP] | FAILED | user: <username> | payload: <base64_encoded_string>`

2. **Attack Signatures (Pattern Matching):**
   You need to extract the base64 payload from each line, decode it, and check if the decoded string contains any of the following malicious patterns (case-insensitive):
   - `union select`
   - `or 1=1`
   - `<script>`

3. **Vulnerability Scanning (Auth Flow Testing):**
   For every payload that matches one of the above signatures, you must test it against our local staging authentication binary located at `/home/user/auth_service`.
   - You must execute `/home/user/auth_service` and pass the **decoded** payload as the first and only command-line argument.
   - Analyze the exit code of `/home/user/auth_service`:
     - If it exits with code `0` (Authentication Bypass successful) or `139` (Segmentation Fault / Memory corruption), mark the payload as `vulnerable: true`.
     - If it exits with any other code (e.g., `1` for properly rejected), mark it as `vulnerable: false`.

4. **Audit Trail Generation:**
   Generate a strict JSON array representing the audit trail and save it to `/home/user/audit_report.json`.
   The JSON must be formatted exactly as an array of objects, containing ONLY the entries that matched the malicious signatures. Ensure chronological order based on the log.
   Each object must have exactly these keys:
   - `timestamp` (string): The exact timestamp from the log file.
   - `decoded_payload` (string): The decoded base64 payload.
   - `vulnerable` (boolean): The result from the vulnerability scan step.

Example output format for `/home/user/audit_report.json`:
```json
[
  {
    "timestamp": "2023-10-25T08:15:30Z",
    "decoded_payload": "admin' OR 1=1 --",
    "vulnerable": true
  }
]
```

Write and run a Rust project in `/home/user/audit_tool` to perform this task. You may use standard crates like `base64`, `regex`, or `serde_json` by configuring your `Cargo.toml`. Create the project, write the code, and run it to produce `/home/user/audit_report.json`.