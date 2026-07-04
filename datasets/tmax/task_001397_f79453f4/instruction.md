You are a security engineer responding to a critical incident. A legacy microservice in your infrastructure was discovered to be vulnerable to the JWT "algorithm=none" bypass. We need to identify which accounts were compromised via this exploit and generate an encrypted revocation list to force credential rotation.

You have been provided with an application access log file located at `/home/user/access.log`. Each line in this file is a JSON object representing an HTTP request, which includes an `Authorization` header containing a JWT.

Additionally, a symmetric encryption key has been placed at `/home/user/rotation_key.key`.

Your task is to write a Python script (e.g., at `/home/user/process_logs.py`) that performs the following steps:
1. Parse the HTTP headers from the JSON log entries in `/home/user/access.log`.
2. Extract the JWT from the `Authorization: Bearer <token>` header.
3. Decode the JWT header and payload (base64url decoded) without verifying the signature.
4. Identify all tokens where the `alg` field in the JWT header is set to `none` (case-insensitive, e.g., `none`, `None`, `NONE`).
5. For each malicious token identified, extract the `username` field from the JWT payload.
6. Compile a list of unique compromised usernames, sort them alphabetically, and join them into a single comma-separated string (e.g., `user1,user2`).
7. Encrypt this string using the Fernet symmetric encryption algorithm (from the `cryptography` Python package) using the key provided in `/home/user/rotation_key.key`.
8. Save the raw encrypted bytes to a file named `/home/user/revocation_list.enc`.

Ensure that your script strictly relies on standard base64 decoding and JSON parsing to inspect the JWTs, and the `cryptography.fernet.Fernet` class for encryption. Only write the final encrypted payload to the output file.