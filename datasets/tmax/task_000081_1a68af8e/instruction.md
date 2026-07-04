You have been assigned to audit and secure a legacy file upload system. The system consists of three services: Nginx, a Flask application, and Redis. The current deployment is misconfigured and vulnerable to path traversal and malicious payload uploads.

Your objective is twofold:
1. Fix the service orchestration so the application runs correctly.
2. Write a precise standalone security auditor script that matches strict security specifications, which will be used to filter uploads.

### Phase 1: Service Configuration
The system files are located in `/app/`.
- **Nginx**: Configured via `/app/nginx.conf`. It should listen on port 8080 and proxy all traffic for `/api/` to the Flask app.
- **Flask App**: Located at `/app/app.py`. It should run on port 5000.
- **Redis**: Should run on the default port 6379.

Currently, `/app/start_services.sh` attempts to start Nginx, Flask, and Redis, but the Nginx configuration is missing the correct `proxy_pass` directive for `/api/` to route to `http://127.0.0.1:5000/`. Modify `/app/nginx.conf` so that requests to `http://127.0.0.1:8080/api/...` are properly proxied. Ensure all services can be started successfully by running `/app/start_services.sh`.

### Phase 2: The Security Auditor Script
The current Flask application does not validate filenames or payloads. You must write a standalone Python script at `/home/user/path_auditor.py` that strictly validates upload requests. 

The script must continuously read single JSON lines from `stdin`. For each line, it must output exactly one JSON line to `stdout`.

**Input Format:**
`{"filename": "<provided_filename_string>", "payload_b64": "<base64_encoded_payload>"}`

**Processing Rules:**
1. **Payload Decoding**: Attempt to decode `payload_b64` using standard Base64. If it is invalid (cannot be decoded), the output status is `"error"`.
2. **Path Traversal Check**: Safely join the provided `filename` to the base directory `/var/uploads`. Compute the absolute, canonicalized path (resolving all `.` and `..`). If the resulting canonical path does not strictly begin with `/var/uploads/` (or is exactly `/var/uploads`), it is a path traversal attempt. The output status is `"malicious"`.
3. **Intrusion Detection**: Scan the decoded binary payload for the exact byte sequence `\xDE\xAD\xBE\xEF`. If this sequence is found anywhere in the payload, the output status is `"malicious"`.
4. **Hashing**: If the payload is successfully decoded and passes the path and intrusion checks, compute the SHA256 hex digest of the decoded binary payload.
5. **Success**: If all checks pass, the output status is `"clean"`.

**Output Format:**
The script must print a single JSON object per input line with exactly these keys:
- `status`: `"clean"`, `"malicious"`, or `"error"`
- `canonical_path`: The computed absolute path as a string (even if malicious or error, as long as it could be computed; if decoding failed before path evaluation, evaluate the path anyway).
- `sha256`: The hex digest of the decoded payload (if `status` is `"clean"`). If `status` is `"malicious"` or `"error"`, this key must be set to `null`.

**Execution:**
Your script must be executable (`chmod +x /home/user/path_auditor.py`) and begin with `#!/usr/bin/env python3`. It must handle multiple lines of input in a loop until `EOF` is reached.

Automated verification will randomly fuzz your `path_auditor.py` script against millions of variations of filenames (including complex traversal payloads) and base64 strings to ensure its output is bit-for-bit identical to our reference security auditor.