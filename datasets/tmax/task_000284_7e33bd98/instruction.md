You are acting as a compliance analyst for a financial organization. We have a legacy system component, provided as a stripped binary executable located at `/app/log_extractor`. When executed, this binary dumps raw, encoded audit events to standard output. 

However, the raw logs contain sensitive Personally Identifiable Information (PII) and potentially malicious XSS payloads injected by attackers into the event streams. 

Your task is to create a secure Python HTTP server that acts as a safe audit trail gateway. 

Requirements:
1. Write a Python script (e.g., `audit_server.py`) that starts an HTTP server listening on `127.0.0.1:8080`.
2. The server must expose a single endpoint: `GET /audit`.
3. **Authentication:** The endpoint must require an `Authorization` header with the exact value `Bearer sec-audit-2024`. If the header is missing or incorrect, return a `401 Unauthorized` status code.
4. **Processing:** When a valid request is received, the server must:
    a. Execute the `/app/log_extractor` binary and capture its standard output.
    b. The output consists of Base64-encoded strings, one per line. Decode each line to reveal a JSON object.
    c. Each JSON object has the following keys: `timestamp`, `user`, and `event_data`.
    d. **Redaction:** Parse the `event_data` field. Find any Social Security Numbers (SSNs) matching the format `XXX-XX-XXXX` (where X is a digit) and replace them with the exact string `[REDACTED_SSN]`.
    e. **XSS Mitigation:** HTML-escape the `event_data` field to neutralize any injection attacks (specifically, replace `<` with `&lt;`, `>` with `&gt;`, `&` with `&amp;`, `"` with `&quot;`, and `'` with `&#x27;`). *Perform redaction before escaping.*
5. **Response:** Return the sanitized sequence of events as a JSON array of objects, with a `200 OK` status code and `Content-Type: application/json`.

You should test your server locally to ensure it properly runs the binary, decodes the payload, sanitizes the data, and returns the correct response over HTTP. Keep the server running in the foreground or background so it can be automatically evaluated.