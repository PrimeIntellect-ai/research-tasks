You are acting as an incident responder and security engineer. We suspect our application was compromised via a JWT vulnerability, and we need you to investigate, remediate the vulnerability, rotate credentials, and perform a file integrity check. 

Perform the following tasks in the `/home/user/` directory:

1. **Log Analysis and Network Policy:**
   Analyze the application access logs located at `/home/user/app/logs/auth.log`. Each line is a JSON object containing `timestamp`, `ip`, and `token` (a JWT). 
   Find the malicious request where the attacker bypassed authentication by sending a JWT with the `alg` header set to `none` (or missing signature) and the payload containing `"role": "admin"`.
   Extract the attacker's IP address and append it to the application's blocklist at `/home/user/app/config/blocklist.json`. The blocklist should be a valid JSON array of strings (e.g., `["192.168.1.1", "10.0.0.5"]`).
   Save ONLY the attacker's IP address as plain text in `/home/user/incident_report/attacker_ip.txt`.

2. **Vulnerability Remediation (Secure Coding):**
   The application's authentication module is located at `/home/user/app/auth.py`. It currently uses the `PyJWT` library to decode tokens but insecurely accepts the `none` algorithm.
   Modify `/home/user/app/auth.py` so that the `decode_token(token, secret)` function explicitly restricts the allowed algorithms to ONLY `HS256`. 

3. **Credential Rotation and Access Control:**
   The compromised key is at `/home/user/app/config/secret.key`.
   Generate a new random 32-byte cryptographically secure secret, encode it in base64, and save it to `/home/user/app/config/new_secret.key`.
   To prevent unauthorized access, set the file permissions of `/home/user/app/config/new_secret.key` to `400` (read-only by the owner).

4. **File Integrity Verification:**
   We have historical keys stored in `/home/user/app/old_keys/` and a SHA256 manifest file at `/home/user/app/keys_manifest.sha256`. 
   The attacker may have backdoored one of the old keys. Verify the SHA256 hashes of the files in the `old_keys` directory against the manifest.
   Identify the single file whose current hash DOES NOT match the hash in the manifest.
   Write the exact filename (e.g., `key_v2.pem`) of the modified file as plain text to `/home/user/incident_report/compromised_key.txt`.