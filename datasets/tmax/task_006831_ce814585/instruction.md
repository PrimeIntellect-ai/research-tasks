You are a security engineer tasked with rotating credentials for a legacy Rust authentication service. The service documentation is lost, and the original developer hardcoded a backup password into the source code. You need to extract the current credentials to proceed with the rotation.

You are provided with the following files:
1. `/home/user/auth_service/access.log` - A web server access log containing recent API requests.
2. `/home/user/auth_service/src/main.rs` - The Rust source code for the authentication service.
3. `/home/user/wordlist.txt` - A list of common passwords used by the development team.

Your tasks are:
1. **Security Log Parsing**: Analyze `access.log` to find the currently valid API key. The key is passed as a query parameter `key=` in the requests. Successful authentications result in a HTTP 200 status code, while failed ones result in 401.
2. **Password Cracking**: Inspect `main.rs` to find a hardcoded SHA256 hash for the backup password. Use the provided `/home/user/wordlist.txt` to crack this hash and find the plaintext password.
3. **CWE Identification**: Identify the standard CWE (Common Weakness Enumeration) ID associated with the vulnerability of using hard-coded credentials in source code.

Once you have gathered all this information, create a JSON report at `/home/user/rotation_report.json` with the following exact structure:

```json
{
  "valid_api_key": "THE_API_KEY_YOU_FOUND",
  "cracked_password": "THE_CRACKED_PLAINTEXT_PASSWORD",
  "cwe_id": "CWE-XXX"
}
```
(Replace `CWE-XXX` with the appropriate CWE identifier, e.g., `CWE-123`).