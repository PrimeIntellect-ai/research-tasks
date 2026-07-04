You are an incident responder investigating a recent breach on one of our internal servers. The attacker left behind a video file that appears to be a screen recording of their terminal during the attack, located at `/app/evidence_041.mp4`. We suspect they compiled a malicious ELF binary, tested its execution, and modified the Content Security Policy (CSP) of our internal testing dashboard to exfiltrate data.

Your task is to analyze the video, extract the necessary information, and reconstruct a sanitized version of the compromised service.

1. **Video Analysis (Pattern Matching & Hash Verification)**: Use `ffmpeg` and Python to process `/app/evidence_041.mp4`. The video contains flashes of text. You need to extract:
   - The SHA-256 hash of the malicious ELF binary the attacker compiled.
   - The exact Content-Security-Policy (CSP) string the attacker injected.
   Write these extracted values to `/home/user/extracted_iocs.json` with keys `binary_sha256` and `injected_csp`.

2. **ELF Analysis**: You will find a suspicious binary located at `/home/user/suspicious_daemon`. Verify its SHA-256 hash against the one found in the video. The binary contains a hidden hardcoded port number used for the attacker's C2 communication. Reverse engineer or analyze the binary to find this integer port number. Write this port to `/home/user/c2_port.txt`.

3. **Service Reconstruction**: Create a secure Python HTTP server (using `http.server` or `Flask`/`FastAPI`) listening on `127.0.0.1:8443` (HTTP, not HTTPS for this exercise).
   - The server must respond to `GET /status` with a 200 OK and a JSON body `{"status": "secure"}`.
   - Every response from this server must include a fixed Content-Security-Policy header. The policy must be the exact *reverse* of the attacker's injected CSP string found in the video (e.g., if the attacker's string was `script-src 'unsafe-inline';`, the secure version should be `default-src 'self';` - wait, to make it programmatic: reverse the entire string character by character).
   - The server must respond to a `POST /report` with the JSON payload. If the payload contains an `ioc_hash` matching the attacker's ELF hash, it should return 403 Forbidden. Otherwise, 200 OK.

Start the service in the background and ensure it is running.