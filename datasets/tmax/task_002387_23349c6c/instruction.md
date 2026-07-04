You are a forensics analyst investigating a compromised Linux host. The server runs a custom Go web application located in `/home/user/webapp/`. 

During the initial triage, the incident response team discovered that the application's file upload handler was susceptible to a path traversal vulnerability. The attacker exploited this to bypass the standard `/home/user/webapp/uploads/` directory and drop an encrypted payload somewhere else on the file system.

Your objectives:
1. Review the web server access logs at `/home/user/webapp/access.log` to identify the malicious upload request and determine where the attacker dropped the file via path traversal.
2. The attacker encrypted the dropped payload using AES-256-GCM. Intelligence suggests the attacker derived their encryption key directly from the application's JWT signing secret to avoid bringing their own keys.
3. Locate the application's configuration file at `/home/user/webapp/config.json` to extract the `jwt_secret` (a 32-byte string).
4. Write a Go program to decrypt the malicious payload. The attacker used standard AES-GCM encryption. The 12-byte nonce (IV) is prepended directly to the beginning of the encrypted file. The rest of the file is the ciphertext (which includes the GCM auth tag at the end).
5. Once decrypted, write the exact plaintext contents of the payload into a new file at `/home/user/report.txt`.

Ensure your Go program correctly parses the prepended nonce and uses the JWT secret as the AES key.