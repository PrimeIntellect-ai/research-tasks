You are a compliance analyst tasked with generating a secure, sanitized audit trail from a legacy company system.

We have a legacy log provider binary located at `/app/audit_daemon`. This is a stripped binary that, when executed, listens on `127.0.0.1:9000` for incoming TCP connections and spits out historical system logs. However, it has several security and compliance issues that you must address to generate the final audit report.

Your objective is to write a Python script at `/home/user/generate_audit.py` that performs the following pipeline:

1. **Service Startup & TLS Wrapping:** 
   The legacy binary does not support encryption. Your script must start `/app/audit_daemon` as a background subprocess. Then, it must generate a self-signed TLS certificate (store it in `/home/user/certs/`) and create a secure TLS wrapper/proxy listening on `127.0.0.1:9443` that forwards traffic to the legacy daemon's port 9000. 

2. **Authentication Flow:**
   The daemon requires a specific, undocumented plaintext authentication token to be sent over the socket before it will stream the logs. You will need to reverse-engineer or analyze the stripped binary at `/app/audit_daemon` to find this hardcoded secret. Your script must connect to the secure `9443` port, perform the TLS handshake, and send this secret string followed by a newline (`\n`).

3. **Sensitive Data Redaction:**
   Once authenticated, the daemon will send raw log lines. These logs contain PII and sensitive credentials that must be redacted for compliance. You must process the stream and replace the exact matches of the following data types with the literal string `[REDACTED]`:
   - IPv4 Addresses (e.g., `192.168.1.100`)
   - 16-digit Credit Card Numbers formatted with hyphens (e.g., `1234-5678-9012-3456`)
   - 32-character hexadecimal API tokens (e.g., `a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4`)

4. **Output:**
   Your script must write the sanitized logs to `/home/user/clean_audit.log`. 

Your solution will be evaluated by an automated testing suite that checks the redaction quality using a strict metric. You must achieve a redaction accuracy (correctly sanitized lines without false positives) of at least 98% against a held-out evaluation log set injected into the daemon during verification.

Constraints:
- Use Python as your primary programming language for the script.
- Ensure your script exits cleanly once the log stream ends (the daemon closes the connection after sending all logs).
- Do not redact data that does not strictly match the three patterns above.