You are a DevSecOps engineer responsible for enforcing policy as code. We have an incident involving leaked logs and a compromised administrator account. You need to sanitize the logs, recover the compromised password for auditing, and expose the sanitized data via a secure internal API.

Follow these steps exactly:

1. **Analyze the Audio Clue**: You have been provided with an intercepted voicemail at `/app/voicemail.wav`. Transcribe the audio (you may use a tool like `whisper` or write a Python script using an available library if needed). The audio dictates:
   - The specific types of PII that must be redacted from our logs.
   - The password generation rule used by the compromised admin (which will help you narrow down the brute-force search space).

2. **Password Cracking**: 
   - A leaked SHA-256 hash of the admin password is saved at `/app/leaked_hash.txt`.
   - Using the generation rule heard in the audio, write a Python script to brute-force the plaintext password.

3. **Sensitive Data Redaction**:
   - You are provided with raw system logs at `/app/raw_logs.json`.
   - Write a Python script to redact the PII mentioned in the audio. Replace the exact sensitive values (Standard US Social Security Numbers formatted as `XXX-XX-XXXX` and 16-digit Credit Card numbers formatted as `XXXX XXXX XXXX XXXX`) with the exact string `[REDACTED]`.

4. **Secure API Deployment**:
   Write and run a Python web server (e.g., using Flask, FastAPI, or Python's built-in `http.server`) listening on `127.0.0.1:8080`.
   The server must implement the following endpoints:
   - `GET /api/logs`: Returns the redacted JSON logs. The response `Content-Type` must be `application/json`.
   - `GET /api/admin_password`: Returns a JSON payload `{"cracked_password": "<the_plaintext_password_you_found>"}`.

   **Security Requirements for the API**:
   - **Authentication**: All endpoints must require an Authorization header with the exact token: `Bearer sec-ops-token-992`. Requests without this token or with an invalid token must return a `401 Unauthorized` status.
   - **Content Security Policy (CSP)**: To enforce our frontend security policies, *every* successful HTTP response from the API must include the following HTTP header:
     `Content-Security-Policy: default-src 'none'; frame-ancestors 'none';`

Ensure your server remains running in the background or foreground so that it can be tested. Do not use external network databases; everything must be self-contained in your scripts.