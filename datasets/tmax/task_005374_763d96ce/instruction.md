You are a security engineer responsible for rotating legacy system credentials before decommissioning an old authentication server.

The previous administrator left a voice memo at `/app/admin_memo.wav` describing the base passphrase. However, the exact legacy password consists of this base passphrase (all lowercase, no spaces) followed by a 4-digit number. 

You need to perform the following steps:
1. **Transcribe and Crack:** Extract the base passphrase from the audio file `/app/admin_memo.wav`. You may install and use whatever transcription libraries you prefer (e.g., `SpeechRecognition`, `pocketsphinx`, or `whisper` if available). Once you have the base passphrase, brute-force the SHA-256 hash located at `/home/user/legacy.hash` to find the exact 4-digit suffix.
2. **Privilege & Policy Audit:** The legacy system previously suffered from XSS and clickjacking. To prevent this in the new rotation system, you must design a strict Content Security Policy.
3. **Multi-Protocol Rotation Service:** Write and run a background service (in any language you choose) that binds to two ports on `127.0.0.1`:
   - **Port 8080 (HTTP):** Must have an endpoint `/csp-check` that returns an HTTP 200 OK status and includes the HTTP header exactly as: `Content-Security-Policy: default-src 'none'; frame-ancestors 'none';` (the body can be empty or "OK").
   - **Port 8081 (Raw TCP):** Must act as the rotation oracle. When a client connects and sends the exact cracked legacy password followed by a newline (`\n`), the server must respond with the new credential string `ROTATED_CRED_9921\n` and close the connection. If the wrong password is sent, it should respond with `DENIED\n`.

Leave this service running in the background. Write a log file to `/home/user/rotation_setup.log` containing the cracked legacy password on the first line.