You are a security engineer handling an incident response and emergency credential rotation. The previous administrator left a voicemail containing the encryption passphrase for the web server logs before their access was revoked.

Your task:
1. Extract the spoken passphrase from the audio file located at `/app/voicemail.wav`. (You may use transcription tools like `whisper` or `ffmpeg` pipelines available in the environment, or install them if necessary).
2. Decrypt the web log file located at `/app/web_traffic.log.enc`. The file was encrypted using OpenSSL with the `aes-256-cbc` cipher and the `-pbkdf2` key derivation function. The password is the exact spoken phrase from the audio (all lowercase, single spaces between words, no punctuation).
3. The decrypted log contains standard web server access logs. Perform pattern matching to identify intrusion attempts. Specifically, you are looking for any requests containing:
   - Directory traversal payloads (e.g., `../` or its URL-encoded equivalents like `%2E%2E%2F` or `%2e%2e%2f`).
   - Cross-Site Scripting (XSS) payloads (e.g., `<script>` or its URL-encoded equivalents like `%3Cscript%3E` or `%3cscript%3e`).
4. Extract the unique IP addresses (the first space-separated field in the log lines) of all clients that sent these malicious payloads.
5. Save the list of unique attacker IP addresses to `/home/user/malicious_ips.txt`, with one IP address per line.

Ensure your final output file exists at the exact path specified. The automated verification system will compare your extracted list of IP addresses against the true list of malicious IPs using an F1 score metric.