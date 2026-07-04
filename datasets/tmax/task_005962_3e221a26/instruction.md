You are a forensics analyst responding to a compromised Linux host. The host was running a custom Go-based file upload service located at `/home/user/upload_server/main.go`. 

We suspect the attacker exploited a vulnerability in this upload handler to perform a path traversal attack, dropping a malicious ELF binary and a configuration token outside the intended `/tmp/uploads/` directory.

We have isolated the suspicious files in the `/home/user/hidden_exfil/` directory:
1. `implant` (an ELF binary)
2. `token.jwt` (a JWT token)

Your task is to:
1. **Code Auditing (CWE Identification):** Review `/home/user/upload_server/main.go` and identify the precise CWE identifier for the vulnerability that allowed the attacker to write files outside the intended directory.
2. **Binary Analysis:** Analyze the `implant` ELF binary to extract the hardcoded JWT secret key. The key is stored as a plaintext string prefixed with `JWT_SECRET=`.
3. **Payload Decoding and Validation:** Write a Go program at `/home/user/analyze.go` that reads `token.jwt`, uses the extracted secret key to validate its signature, and decodes the payload.
4. **Reporting:** Generate a final forensics report at `/home/user/report.json` with the following exact JSON schema:

```json
{
  "vulnerability_cwe": "CWE-XXX",
  "extracted_key": "the_secret_key_value",
  "decoded_payload_user": "the_user_value_from_the_jwt_payload"
}
```
(Replace XXX, the_secret_key_value, and the_user_value_from_the_jwt_payload with your actual findings).

Requirements:
- Ensure the JSON file is valid.
- You do not need to fix the vulnerable Go code, only audit it to find the CWE.
- Standard JWT libraries (like `github.com/golang-jwt/jwt/v5`) can be downloaded using `go get` if you choose to write a Go script for decoding.