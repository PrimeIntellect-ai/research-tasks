You are a penetration tester auditing a local custom authentication server. 

We have provided the server source code at `/home/user/server.py` and a sample log file containing recent API requests at `/home/user/api_logs.txt`. The server implements a custom JSON Web Token (JWT) validation mechanism. 

Your tasks are:
1. **Vulnerability Analysis & Exploitation:** Start the server on `127.0.0.1:8080`. Analyze `/home/user/server.py` to identify a cryptographic/authentication flaw in how it handles JWT algorithms.
2. Write an exploit script (or use tools like `curl` and `python3`) to forge a token for the user "admin" with the role "admin". 
3. Send a GET request to `http://127.0.0.1:8080/flag` using your forged token in the `Authorization: Bearer <token>` header. The server will return a secret flag if successful. Save this exact flag string to `/home/user/flag.txt`.
4. **Sensitive Data Redaction:** Before you submit your findings, you must redact the client's log file located at `/home/user/api_logs.txt`. Find all validly formatted JWTs (strings consisting of three base64-url encoded segments separated by periods) and replace them with the exact string `[REDACTED_JWT]`. Save the sanitized logs to `/home/user/redacted_logs.txt`.
5. **Checksum Verification:** Calculate the SHA-256 hash of `/home/user/redacted_logs.txt` and output only the hex digest into `/home/user/hash.txt`.

Ensure the server process is properly managed (you can run it in the background while you exploit it).