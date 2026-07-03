You are acting as a compliance analyst. You need to process a raw access log file to generate a secure, verified audit trail. The raw logs contain base64-encoded payloads that include sensitive Data (Credit Card numbers) and HMAC tokens that verify the integrity of each log entry. 

Your task is to write a Python script (and use standard bash commands) to process this log and produce the final artifacts.

Here are the details:
1. **Inputs:**
   - Raw log file: `/home/user/raw_access.log`
   - Secret key file: `/home/user/.secret_key` (contains the plaintext secret key used for HMAC validation)

2. **Log Format:**
   Each line in `/home/user/raw_access.log` has the following pipe-separated format:
   `IP_ADDRESS | TIMESTAMP | HMAC_TOKEN | BASE64_PAYLOAD`

3. **Validation (Token Verification):**
   - The `HMAC_TOKEN` is an HMAC-SHA256 hex digest.
   - The message used to generate the HMAC is the exact string: `IP_ADDRESS|TIMESTAMP|BASE64_PAYLOAD`
   - You must validate each line using the secret key from `/home/user/.secret_key`.
   - If the token is **invalid**, the log entry must be dropped, and its `IP_ADDRESS` should be added to a firewall blocklist.

4. **Decoding & Redaction:**
   - For valid log entries, decode the `BASE64_PAYLOAD`. The decoded payload is a JSON string containing an action and a credit card number, e.g., `{"user": "alice", "cc": "1234-5678-9012-3456"}`.
   - Redact the credit card number so that only the last 4 digits are visible. Replace the first 12 digits with `X`s. The format must become `XXXX-XXXX-XXXX-3456`.
   - Re-encode the redacted JSON string back into base64. Ensure no extra newlines are added during base64 encoding.

5. **Outputs:**
   - Create a JSON file at `/home/user/audit_trail.json` containing a JSON array of the valid, redacted log entries. Each object in the array should have the keys: `"ip"`, `"timestamp"`, and `"redacted_payload"` (the new base64 string).
   - Create a text file at `/home/user/blocked_ips.txt` containing the unique IP addresses that had invalid HMAC tokens, one per line, sorted alphabetically.
   - Generate a SHA-256 checksum of the `/home/user/audit_trail.json` file and save it to `/home/user/audit_trail.sha256` in the standard `sha256sum` format.

Ensure your processing is fully automated. Do not modify the original log file.