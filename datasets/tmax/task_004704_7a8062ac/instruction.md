You are acting as a security auditor responding to a recent incident. We have received an audio recording from an on-site admin detailing an intrusion, located at `/app/incident_report.wav`. 

Your objectives are as follows:
1. **Audio Analysis**: Transcribe or extract the spoken content of `/app/incident_report.wav`. The audio contains a spoken secret token that you will need for your final report.
2. **File Integrity Verification**: We suspect some files in `/home/user/webroot` were tampered with. Check the SHA256 hashes of all `.js` and `.html` files in this directory against the known-good hashes provided in `/home/user/known_hashes.txt`. Note down which file was modified.
3. **Intrusion Detection**: Analyze the log file at `/home/user/access.log` using pattern matching. Find the IP address that made requests containing the string `eval(` or `base64_decode(`. Note down the IP address of the attacker.
4. **Audit Reporting Service**: You must write a pure Bash script (using `nc` or similar coreutils, no Python/Node.js) that starts an HTTP server listening on `127.0.0.1:8080`. 
   - The server must respond to `GET /audit` requests.
   - The HTTP response must include a strict Content Security Policy enforcement header: `Content-Security-Policy: default-src 'none';`.
   - The response body must be in JSON format: `{"status": "audited", "tampered_file": "<filename>", "attacker_ip": "<ip>", "secret_token": "<token_from_audio>"}`.
   - Keep this server running in the background so our automated verification suite can query it.

Ensure your Bash HTTP server correctly handles standard HTTP GET requests and formats the headers properly (including `\r\n`).