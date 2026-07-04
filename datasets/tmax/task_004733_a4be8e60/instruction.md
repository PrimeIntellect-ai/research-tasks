You are a security auditor tasked with analyzing a custom authentication service and checking its permissions. A legacy login flow contains a potential vulnerability where hardcoded credentials might be extractable and usable to bypass network policies.

You have been provided with the following files:
- `/home/user/auth_binary`: A compiled ELF executable of the authentication service.
- `/home/user/wordlist.txt`: A small dictionary of common passwords.
- `/home/user/policy.conf`: A mock firewall and network policy configuration file.

Perform the following tasks:
1. **Binary Analysis**: Analyze the `/home/user/auth_binary` executable. Extract the hardcoded password hash (which is prefixed with `HASH:`) and the cryptographic salt (prefixed with `SALT:`). 
2. **Password Cracking**: The authentication service verifies passwords by computing the SHA-256 digest of the password concatenated with the salt (i.e., `SHA256(<password><salt>)`). Write a Bash script to brute-force and crack the password using the provided `/home/user/wordlist.txt`.
3. **Token Generation**: Using the cracked password as a secret key, generate a valid session token for the admin user. The token must be the HMAC-SHA256 hex digest of the exact string `admin_access` using the cracked password as the HMAC key. 
   - Save the raw hex value of this token (lowercase, no prefix or trailing spaces) to a new file at `/home/user/admin_token.txt`.
4. **Network Policy Configuration**: Modify the mock firewall policy file `/home/user/policy.conf`. The file currently begins with the line `DENY ALL`. Replace that first line with `ALLOW ADMIN <token>`, where `<token>` is the exact hex token you generated in the previous step. Leave the rest of the file unchanged.

Ensure your token generation and string concatenations do not include unwanted newline characters.