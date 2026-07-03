You are an incident responder investigating a recent breach on a Linux web server. The attacker exploited a path traversal vulnerability and left behind a voicemail snippet. You need to analyze the evidence, correlate logs, crack the attacker's authentication, and deploy a patched replacement service.

Your task is broken down into three main phases:

**Phase 1: Evidence Analysis & Password Cracking**
1. You have been provided an audio file at `/app/intercepted_call.wav`. Transcribe this audio (you may install tools like `whisper`, `ffmpeg`, or similar) to discover the format of the attacker's secret password.
2. The attacker's password hash (SHA256) is recorded on the last line of the log file at `/app/system_auth.log`. Using the format hint from the audio, perform a dictionary or brute-force attack to crack this hash.

**Phase 2: Log Correlation**
1. Parse `/app/nginx_access.log`. Identify the single IPv4 address that successfully exploited a path traversal vulnerability to download the server's shadow file (look for a `200` HTTP status code on a request attempting to traverse to `/etc/shadow`).

**Phase 3: Deploying a Secure Replacement Service**
1. Write and run a Python-based HTTP web service (using Flask, FastAPI, or standard library) that listens on `0.0.0.0:8080`.
2. The service must expose a `POST /api/v1/upload` endpoint.
3. **Authentication**: Every request to this endpoint must include an `X-Incident-Auth` HTTP header formatted exactly as `<CRACKED_PASSWORD>:<ATTACKER_IP>` (e.g., `secret123:192.168.1.1`). If the header is missing or incorrect, return a `401 Unauthorized` status code.
4. **Content Security Policy**: Every response from your server (regardless of status code) MUST include the following security header exactly: `Content-Security-Policy: default-src 'self'; script-src 'none';`
5. **Path Traversal Protection**: The endpoint should accept a JSON payload with a `filename` key (e.g., `{"filename": "report.pdf"}`). 
   - If the `filename` value contains `../` or `..\` (path traversal sequences), return a `400 Bad Request` status code.
   - If the `filename` is safe, return a `200 OK` status code.

Leave your Python server running in the background or foreground so that the automated verification system can test it. Ensure it listens on `0.0.0.0` port `8080`.