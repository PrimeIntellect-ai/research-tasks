You are an incident responder investigating a recent breach on a critical web server. The attacker left a voice message for a co-conspirator, and we have recovered the audio file at `/app/voicemail.wav`. We also have the web server logs at `/app/access.log`, the web directory at `/app/www/`, and an integrity manifest at `/app/manifest.sha256`.

Your objectives are:

1. **Audio Analysis**: Transcribe the audio file `/app/voicemail.wav` (using `whisper` or any available transcription tool in your environment). The message contains a secret backdoor passphrase.
2. **File Integrity & Vulnerability Analysis**: 
   - Verify the integrity of the files in `/app/www/` using `/app/manifest.sha256`. Identify which file was modified by the attacker.
   - Analyze `/app/access.log` to find the malicious injection payload that the attacker used to compromise the system. The payload is a distinct SQL injection string.
3. **Honeypot Deployment**: 
   To trap the attacker when they return, write and run a multi-protocol honeypot service in Python or Bash that listens on two ports simultaneously:
   - **HTTP Service (`127.0.0.1:8080`)**: Must listen for GET requests. If the request includes the HTTP header `X-Passphrase` with the exact secret passphrase extracted from the audio (in lowercase, no punctuation), the server must respond with a `200 OK` and a plaintext body containing exactly the *original* SHA256 hash (from the manifest) of the compromised file. If the header is missing or incorrect, return a `403 Forbidden`.
   - **TCP Service (`127.0.0.1:8081`)**: Must listen for raw TCP connections. If the client sends the exact string `SEND_PAYLOAD\n`, the server must reply with the exact SQL injection payload found in the access log, followed by a newline, and then close the connection.

Run the honeypot in the background so it remains active. Do not write the solution to a file without executing it. Ensure the service binds to `127.0.0.1` and the ports specified.