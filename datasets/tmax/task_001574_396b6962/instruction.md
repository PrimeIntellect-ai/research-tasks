You are a security engineer tasked with rotating credentials for a legacy internal system. You must analyze the existing binary, authenticate with the legacy server, rotate the key, verify the new key's integrity, and audit a supporting script for vulnerabilities.

Here are your instructions:

1. **Extract Old Credentials**:
   Analyze the ELF binary located at `/home/user/legacy_auth_client`. It contains a hardcoded old API key in the format `OLD_API_KEY=<secret>`. Find this secret key.

2. **Authenticate and Rotate**:
   A local key-rotation server is running at `http://127.0.0.1:8080`.
   - First, make a `GET` request to `http://127.0.0.1:8080/auth` and include the extracted key in the `X-Old-Key` HTTP header. 
   - If successful, the server will return a `Set-Cookie` header containing a `session_id`.
   - Next, make a `POST` request to `http://127.0.0.1:8080/rotate` and include this `session_id` cookie.
   - The server will respond with a JSON payload containing `new_key` and `sha256_checksum`.

3. **Verify Integrity**:
   Save the exact string value of `new_key` into a file at `/home/user/new_key.txt` (no trailing newline). 
   Compute the SHA-256 hash of `/home/user/new_key.txt`. 
   If the computed hash matches the `sha256_checksum` provided in the JSON payload, write the exact word `VERIFIED` to `/home/user/integrity_check.txt`. If it does not match, write `FAILED`.

4. **Code Auditing (CWE Identification)**:
   Review the Python script at `/home/user/auth_handler.py`. This script contains a cryptographic flaw related to how it hashes passwords. Identify the exact CWE (Common Weakness Enumeration) ID for this vulnerability (e.g., "Use of Weak Hash" or "Use of a Broken or Risky Cryptographic Algorithm").
   Write the CWE ID in the format `CWE-XXX` (where XXX is the number) to `/home/user/cwe_vulnerability.txt`. Do not include any other text in this file.