You are assisting a compliance analyst with generating an audit trail for a recent security incident involving forged authentication tokens. 

We have captured several JSON Web Tokens (JWTs) from our access logs. They are stored in `/home/user/jwt_logs.txt`, with one token per line. We suspect that an attacker bypassed authentication by exploiting a vulnerability where the application accepts tokens with the "none" algorithm.

Perform the following tasks:
1. Write a Python script at `/home/user/audit.py` that reads `/home/user/jwt_logs.txt`.
2. The script must decode the header of each JWT (the portion before the first dot `.` which is Base64URL encoded) and parse it as JSON.
3. Identify any tokens where the `alg` (algorithm) field in the header is set to `"none"` (this should be a case-insensitive check, e.g., `"none"`, `"NONE"`, `"None"`).
4. The script must write an audit trail to `/home/user/vulnerable_tokens.json`. This file must contain a single JSON array of strings, where each string is the exact, complete vulnerable JWT from the log file. Do not include tokens that use secure algorithms (like HS256).
5. Run your script to generate the JSON file.
6. To enforce access control on the sensitive audit trail, change the file permissions of `/home/user/vulnerable_tokens.json` to strictly read-only for the owner, and no permissions for anyone else (`0400`).
7. As part of our remediation plan, generate a new ED25519 SSH keypair that we will use to distribute our new token signing application. Save the keypair to `/home/user/new_jwt_key` (with the public key automatically becoming `/home/user/new_jwt_key.pub`). Do not set a passphrase.

Ensure your Python script relies only on standard libraries (e.g., `base64`, `json`). Note that Base64URL encoding might require padding (`=`) to be added before standard Base64 decoding works in Python.