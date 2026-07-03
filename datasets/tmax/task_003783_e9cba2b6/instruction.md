You are a security engineer assigned to rotate credentials and patch a vulnerable authentication mechanism after an incident. An attacker managed to compromise several user sessions due to a weak cryptographic hashing algorithm (MD5) used for token generation (CWE-327).

Your environment consists of a multi-service application running locally:
1. A Redis cache (running on port 6379) which stores active user sessions.
2. A Flask API (running on port 5000) which serves user requests and verifies tokens.

The startup script for these services is `/app/start.sh`, which has already been executed.

You must complete the following multi-stage workflow:

**Stage 1: Log Parsing and Session Revocation**
1. Analyze the security access logs located at `/app/logs/access.log`.
2. Identify all requests where the `User-Agent` header exactly matches the known malicious actor `"EvilBot/1.0"`.
3. Extract the compromised session tokens from those log entries. The log format is:
   `[TIMESTAMP] IP - User-Agent - SessionID:<TOKEN> - Endpoint`
4. Connect to the local Redis instance and delete the keys corresponding to the compromised sessions. The Redis keys are formatted as `session:<TOKEN>`.

**Stage 2: Code Auditing and Configuration Rotation**
1. The Flask API reads its configuration from `/app/config/settings.json`. Update this file to rotate the compromised secret key. Change the `"api_secret"` value to exactly `"Secr3t_HMAC_v2_991"`.
2. You must restart the Flask API service for the changes to take effect without stopping Redis. The Flask API is managed via a systemd user service or a background process. You can restart it by killing the `flask` process and running `/app/start_flask.sh &`.

**Stage 3: Token Generator Implementation**
The old token generation logic is fundamentally flawed. You must create a standalone CLI tool that generates mathematically secure, bit-exact tokens according to the new standard. 

Create a Python script at `/home/user/generate_token.py`.
This script must accept exactly two command-line arguments:
* `--user` (the username string)
* `--time` (a Unix timestamp integer)

The script must print ONLY the generated token to standard output, with no trailing newline or extra whitespace.
The new token generation algorithm must be:
`HMAC-SHA256(secret_key, message)`
Where:
* `secret_key` is the new rotated secret: `"Secr3t_HMAC_v2_991"` (encoded as UTF-8)
* `message` is the strict concatenation of the username, a colon (`:`), and the timestamp (e.g., `alice:1700000000`), encoded as UTF-8.
* The output must be the lowercase hexadecimal representation of the HMAC digest.

Ensure `/home/user/generate_token.py` is executable and rigorously adheres to the input and output requirements, as it will be fuzz-tested against a compiled reference oracle.