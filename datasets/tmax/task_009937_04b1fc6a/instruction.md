You are a security engineer tasked with rotating a compromised, weak credential for a legacy application. The old API key is known to be vulnerable because it uses a weak generation pattern: it always starts with the hexadecimal string `DEAD` followed by exactly 12 lowercase hexadecimal characters (e.g., `DEADbeef12345678`).

You need to perform the following actions using standard Linux bash commands:

1. **Redact Logs:** The application has been leaking this old key into its log file located at `/home/user/app.log`. Find all instances of this specific 16-character weak key pattern in `/home/user/app.log` and replace them entirely with the exact string `[REDACTED]`. Modify the file in place.
2. **Rotate Credential:** The configuration file located at `/home/user/config.ini` currently contains the old key on a line starting with `API_KEY=`. 
3. **Generate New Key:** Generate a new, secure, 32-character lowercase hexadecimal string (you can use `/dev/urandom` and standard utilities). 
4. **Update Config:** Replace the old key in `/home/user/config.ini` with your newly generated key. Modify the file in place.
5. **Output Verification:** Save your newly generated 32-character hexadecimal key to a file at `/home/user/new_key.txt` (the file should contain *only* the new key and an optional newline).

Ensure you only rely on standard bash built-ins and coreutils (like `sed`, `grep`, `tr`, `head`, `xxd`, etc.).