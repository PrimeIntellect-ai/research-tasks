You are acting as a network security engineer investigating a recent breach. We suspect an attacker exploited a file upload endpoint susceptible to path traversal, dropped encrypted payloads, and modified system binaries to escalate privileges. 

Your objective is to build a Python tool that analyzes the captured traffic, decrypts the attacker's payloads, verifies system integrity, and audits file permissions.

You have been provided with the following files:
1. `/home/user/traffic_logs.json`: An export of web traffic logs. Each entry contains `request_id`, `method`, `url`, `status`, and a `payload` field (which is base64 encoded).
2. `/home/user/secret.key`: A file containing a 16-byte key used by the application (and potentially the attacker) to encrypt payloads.
3. `/home/user/system/`: A directory containing critical system files.
4. `/home/user/system_hashes.txt`: A text file containing the known-good SHA256 hashes of the files in the `/home/user/system/` directory. Format: `hash  filename`.

Write a Python script (you can install dependencies like `cryptography` via pip) that performs the following steps:

**Phase 1: Intrusion Detection**
Parse `/home/user/traffic_logs.json`. Identify all requests that meet BOTH of the following criteria:
- The `url` contains path traversal sequences (e.g., `../` or `..%2f` - case-insensitive).
- The `status` code is `201`.

**Phase 2: Decryption**
For the malicious requests identified in Phase 1, extract the `payload`. 
- Base64 decode the payload.
- Decrypt it using AES-128-CBC. The encryption key is the raw text content of `/home/user/secret.key`. The first 16 bytes of the decoded payload act as the Initialization Vector (IV), and the remainder is the ciphertext. PKCS7 padding was used.
- Decode the decrypted bytes to a UTF-8 string.

**Phase 3: Integrity and Privilege Escalation Audit**
Analyze the files in `/home/user/system/`.
- Calculate the SHA256 hash of each file and compare it against the hashes listed in `/home/user/system_hashes.txt`. Note which files have mismatched hashes.
- Check the permissions of each file. Identify any file that has the SUID bit set.

**Phase 4: Reporting**
Output your findings to a JSON file located at `/home/user/incident_report.json` with the exact following structure:
```json
{
  "malicious_requests": ["req_id_1", "req_id_2"],
  "decrypted_payloads": ["decrypted_string_1", "decrypted_string_2"],
  "tampered_files": ["/home/user/system/filename1"],
  "suid_files": ["/home/user/system/filename2"]
}
```
*Note:* Provide absolute paths for the files in the `tampered_files` and `suid_files` lists. Keep the arrays sorted in ascending alphabetical order.