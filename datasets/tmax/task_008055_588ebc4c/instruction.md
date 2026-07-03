You are a penetration tester performing a local exploit simulation and data exfiltration exercise.

We have a local tool located at `/home/user/vulnerable_app.py`. This tool simulates a service that fetches a JSON configuration from a provided URL and reads a local file specified in the `file_to_read` field of the JSON. It has a path traversal/arbitrary file read vulnerability.

Your task is to craft an automated exploit script that serves a malicious payload over a secure connection, triggers the vulnerability, captures sensitive data, redacts it, and securely stores the result.

Perform the following steps:

1. Create a directory at `/home/user/certs` and set its permissions to `700`.
2. Generate a self-signed RSA 2048-bit TLS/SSL certificate (`cert.pem`) and private key (`key.pem`) valid for 365 days, and place them in `/home/user/certs/`.
3. Create a Python script at `/home/user/run_exploit.py` that does the following when executed:
   - Starts a local HTTPS server on `localhost` port `8443` using the certificate and key you generated.
   - Serves a JSON payload at the root path (`/` or any path) that exploits the vulnerability. The payload must instruct the vulnerable app to read `/home/user/secret.txt`.
   - While the server is running in the background, the script must invoke `/home/user/vulnerable_app.py https://localhost:8443/` using the `subprocess` module.
   - Capture the standard output of `vulnerable_app.py` (which will contain the contents of `secret.txt`).
   - Redact any 16-digit credit card numbers found in the output. Credit card numbers are formatted as `DDDD-DDDD-DDDD-DDDD` (where D is a digit). Replace the entire credit card number with `XXXX-XXXX-XXXX-XXXX`.
   - Write the redacted output to a file located at `/home/user/loot.txt`.
   - Ensure the permissions of `/home/user/loot.txt` are strictly set to read and write for the owner only (`0600`).
4. Run your `/home/user/run_exploit.py` script so that `/home/user/loot.txt` is successfully generated.

Ensure your script is robust and cleanly shuts down the HTTPS server after capturing the data. Do not alter `/home/user/vulnerable_app.py` or `/home/user/secret.txt`.