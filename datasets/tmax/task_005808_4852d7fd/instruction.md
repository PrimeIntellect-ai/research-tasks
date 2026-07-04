You are a security engineer handling an incident response. We suspect that one of our internal backend services was exploited via an open redirect vulnerability in its login flow, which led to the leakage of an active session token. 

You have been provided with the API gateway access log at `/home/user/gateway.log`. The log format is:
`CLIENT_IP [TIMESTAMP] BACKEND_PORT "HTTP_METHOD URI HTTP_VERSION" HTTP_STATUS BYTES "SESSION_TOKEN"`

Your task involves three steps:
1. **Log Analysis:** Parse `/home/user/gateway.log` to identify the successful open redirect exploit. A successful exploit is defined as a request to the `/login` endpoint that returns a `302` HTTP status code, where the `redirect` query parameter is an absolute external URL (starts with `http://` or `https://`).
2. **Data Extraction:** Identify the `BACKEND_PORT` of the vulnerable service and the leaked `SESSION_TOKEN` from that specific log entry.
3. **Credential Rotation:** Write a Bash script at `/home/user/rotate_token.sh` that generates a new master token.
   - The script must accept exactly two arguments: the backend port and the leaked token (e.g., `./rotate_token.sh <port> <token>`).
   - The script must compute the SHA-256 hash of the exact string `<port>:<token>:secret_salt_2024` (ensure no trailing newlines are included in the hashed input).
   - The script must write ONLY the resulting 64-character lowercase hex string to `/home/user/new_token.txt`.

Finally, execute your script using the port and token you discovered to create the `/home/user/new_token.txt` file.

Make sure your script `/home/user/rotate_token.sh` is executable.