You are a network security engineer investigating suspicious traffic on an internal network. We have intercepted an encrypted radio transmission, which has been demodulated and saved as an audio file at `/app/intercept.wav`. 

Your task is to build a Go-based traffic inspection service that enforces the security policies dictated in the audio intercept and performs real-time payload sanitization and vulnerability scanning.

Step 1: Audio Analysis
Extract the spoken contents from `/app/intercept.wav`. The audio contains two critical pieces of information:
1. The secret admin authentication token.
2. A specific malicious domain name that must be blocked.

Step 2: Develop the Inspection Service
Write and run a Go web server that listens on exactly `127.0.0.1:8080`. The server must expose a single HTTP POST endpoint: `/inspect`.

Endpoint specifications:
* **Authentication**: All requests must include the header `Authorization: Bearer <TOKEN>`, where `<TOKEN>` is the exact token transcribed from the audio (converted to lowercase, no spaces). If the token is missing or incorrect, return HTTP 401 Unauthorized.
* **Input**: The endpoint will receive a JSON payload with the following structure:
  ```json
  {
    "domain": "string",
    "cert_chain_pem": "string",
    "payload": "string",
    "user_agent": "string"
  }
  ```
* **Processing Rules**:
  1. **Blocked Domain**: If the `domain` exactly matches the malicious domain from the audio, the traffic must be blocked.
  2. **Certificate Validation**: The `cert_chain_pem` contains a sequence of PEM-encoded X.509 certificates (leaf first, followed by intermediates/roots). Parse the leaf certificate. Verify that the leaf certificate is valid for the requested `domain` (check the Common Name / DNS Names). If it does not match, the traffic must be blocked. (You do not need to verify the cryptographic signatures of the chain for this exercise, only that the leaf certificate's hostname matches the `domain`).
  3. **Injection/XSS Analysis**: Analyze the `user_agent` string. If it contains the exact substrings `<script>` or `' OR 1=1`, flag the request as containing an injection attack.
  4. **Sensitive Data Redaction**: Scan the `payload` string for any 16-digit credit card numbers (contiguous digits, e.g., `1234567812345678`). Replace all such occurrences with `XXXX-XXXX-XXXX-XXXX`.

* **Output**: Return a JSON response with HTTP 200 OK (for authenticated requests, regardless of block status) in this format:
  ```json
  {
    "status": "string",
    "redacted_payload": "string"
  }
  ```
  The `status` field must be one of the following (evaluated in this order of precedence):
  - `"blocked_domain"` (if rule 1 fails)
  - `"invalid_cert"` (if rule 2 fails)
  - `"blocked_injection"` (if rule 3 fails)
  - `"allowed"` (if all rules pass)

Keep the server running in the foreground or background so it can be tested. Write your Go code in `/home/user/inspector.go` and execute it.