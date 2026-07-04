You are acting as a penetration tester and security engineer. We have a legacy vulnerability scanner provided as a stripped, UPX-packed binary located at `/app/legacy_scanner`. This proprietary tool is useful for identifying service misconfigurations, but it has two major issues:
1. It outputs its scan results in a proprietary encrypted hex format.
2. The decrypted results often contain sensitive data (like leaked passwords or API tokens) that must not be exposed to downstream systems.

Your task is to build a secure API wrapper around this binary using **Go**.

### Requirements:

1. **Reverse Engineer / Cryptanalysis:**
   Analyze `/app/legacy_scanner`. You will find that running `/app/legacy_scanner <ip> <port>` outputs a hex string. You must determine the weak encryption algorithm used by the binary to obfuscate its output (hint: it's a simple byte-level operation). 

2. **Secure Wrapper Service:**
   Write a Go web service that listens on `127.0.0.1:9090`. 
   It must expose a `POST` endpoint at `/api/scan`.
   The endpoint expects a JSON payload: `{"target_ip": "127.0.0.1", "target_port": "<port>"}`.

3. **Process Execution & Redaction:**
   When a request is received, your Go service should:
   - Execute `/app/legacy_scanner` with the provided IP and port. 
   - Ensure the process execution is bounded by a 5-second timeout to prevent hanging scans.
   - Capture the hex output, decode it, and decrypt it back into plaintext JSON.
   - Parse the resulting JSON and perform **sensitive data redaction**: any JSON key that exactly matches `"password"`, `"api_token"`, or `"secret"` must have its value replaced with the exact string `"[REDACTED]"`.
   
4. **Response:**
   The HTTP endpoint must return the decrypted, fully redacted JSON object with an `HTTP 200 OK` status and `Content-Type: application/json`. If the scanner process times out or fails, return `HTTP 500`.

Build and run your Go service in the background so it is actively listening on `127.0.0.1:9090`. Do not stop the service once it is running, as an automated verifier will send HTTP requests to it to validate your work.