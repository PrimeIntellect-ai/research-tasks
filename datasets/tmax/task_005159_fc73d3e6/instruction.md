You are acting as a security auditor for a legacy system. During an audit, you discovered a proprietary, undocumented binary at `/app/acl_checker` that the system uses to evaluate access control requests. You need to build a secure, modern API wrapper around this binary to enforce additional security controls, integrity checks, and audit logging.

Create a Python HTTP API service that listens on `127.0.0.1:9000`. The service must expose a single endpoint: `POST /check_access`.

The endpoint will receive JSON payloads in the following format:
```json
{
  "file_path": "/absolute/path/to/target_file",
  "auth_token": "user_provided_token_string",
  "justification": "Text describing why access is needed, e.g., checking SSN 555-12-3456"
}
```

Your Python wrapper must perform the following security pipeline in order:
1. **Intrusion Detection (Pattern Matching):** Inspect the `file_path`. If it contains any path traversal sequences (specifically `..` or `//`), immediately respond with HTTP 403 Forbidden and the JSON `{"error": "Malicious path detected"}`.
2. **File Integrity Verification:** The system has a known-good ledger at `/home/user/secure_ledger.txt`. Each line contains a SHA256 hash followed by two spaces and an absolute file path. If the `file_path` is not in the ledger, or if the actual file's current SHA256 hash does not exactly match the hash in the ledger, respond with HTTP 403 Forbidden and `{"error": "Integrity check failed"}`.
3. **Data Redaction:** The `justification` field may contain sensitive US Social Security Numbers. Before passing it to any log, you must redact any pattern matching `XXX-XX-XXXX` (where X is a digit) by replacing all digits with asterisks (`***-**-****`).
4. **Legacy Access Check:** Once the path and integrity are validated, your wrapper must invoke the legacy binary to determine access. Execute `/app/acl_checker <file_path> <auth_token>`. The binary exits with code `0` if access is granted, and code `1` if denied.
5. **Audit Logging:** Append a log entry to `/home/user/access_audit.log` exactly in this format:
   `[GRANTED|DENIED] - File: <file_path> - Justification: <redacted_justification>`
6. **Response:** Return HTTP 200 OK with the JSON payload:
   `{"access": "GRANTED" | "DENIED", "logged_justification": "<redacted_justification>"}`

You may install any required Python packages (e.g., `Flask`, `FastAPI`). Make sure your service is running and listening on the specified port when you finish. Do not modify the legacy binary.