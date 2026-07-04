You are a compliance analyst investigating a past security incident. An attacker exploited a file upload handler susceptible to a path traversal vulnerability to drop an encrypted archive on the system. You need to retrace their steps, decode their payload, and generate an audit trail report.

All investigation files are located in `/home/user/audit_investigation`.

Here are your objectives:

1. **Token Validation**: The attacker captured several session tokens, which are stored in `/home/user/audit_investigation/captured_tokens.txt`. The tokens are standard HS256 JWTs signed with the secret key found in `/home/user/audit_investigation/jwt_secret.txt`. You must write a Python script to validate these tokens. Only one token is valid, not expired, and belongs to the user `admin`. Extract the `jti` (JWT ID) of this specific token.

2. **Password Cracking**: The attacker uploaded a malicious zip file via path traversal. It bypassed the intended `/home/user/audit_investigation/uploads/` directory and was saved as `/home/user/audit_investigation/system/backup.zip`. This zip file is protected by a 4-digit numeric PIN. You must brute-force the password to extract its contents.

3. **Payload Decoding**: Inside the zip file is a file named `payload.txt`. The text inside is encoded. The attacker first converted the plain text to hexadecimal representation, and then Base64-encoded that hex string. You must reverse this process to recover the original plaintext message.

4. **Audit Trail Generation**: Create an audit report at `/home/user/audit_report.json`. The file must be valid JSON strictly matching this format:
```json
{
  "admin_jti": "<the jti of the valid admin token>",
  "zip_pin": "<the 4-digit pin used to crack the zip>",
  "decoded_payload": "<the final decoded plaintext message>"
}
```

Ensure the final report exists at `/home/user/audit_report.json` with the exact keys specified above.