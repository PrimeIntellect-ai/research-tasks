You are a compliance analyst tasked with generating clean audit trails. We have a legacy system that periodically spawns processes and, unfortunately, leaks sensitive authentication tokens via command-line arguments. 

Your task is to create a Python script at `/home/user/audit_redactor.py` that processes a raw audit log and redacts valid leaked tokens.

Here are the details:
1. There is an ELF binary located at `/home/user/legacy_worker`. This binary is known to contain the hardcoded HMAC-SHA256 secret key used to sign the system's JWTs (JSON Web Tokens). The secret key is a string starting with `COMPLIANCE_KEY_`. You must extract this secret from the binary.
2. The raw audit log is located at `/home/user/raw_audit.log`. Each line represents a logged command execution.
3. The log contains command-line arguments, some of which take the form `--token <JWT>`. 
4. Your Python script (`/home/user/audit_redactor.py`) must read `/home/user/raw_audit.log`, find all tokens passed via `--token`, and validate their HMAC-SHA256 signatures using the secret extracted from the binary. (Note: standard JWT format is `base64url(header).base64url(payload).base64url(signature)`).
5. If a token has a valid signature, you must replace the token in the log line with `[REDACTED]`. If the signature is invalid or it is not a valid JWT, leave it exactly as is.
6. The script should output the redacted log to `/home/user/clean_audit.log`.

Constraints:
- Only use Python standard libraries (e.g., `base64`, `hmac`, `hashlib`, `json`, `re`). Do not use third-party packages like `PyJWT`.
- Ensure base64url decoding adds the correct padding if necessary.
- Run your script to generate `/home/user/clean_audit.log`.