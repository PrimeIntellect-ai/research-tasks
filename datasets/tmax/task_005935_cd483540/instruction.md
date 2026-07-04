You are a release manager preparing a local deployment service to serve release notes to internal tools. You need to process the latest release notes, set up a secure local Python server to serve them, and place it behind a rate-limited reverse proxy. 

Please accomplish the following:

1. **Process Release Notes (Diffing, Sorting, Encoding)**
   You have two files: `/home/user/v1.txt` and `/home/user/v2.txt`.
   - Identify all lines that exist in `v2.txt` but NOT in `v1.txt`.
   - Sort these new lines alphabetically.
   - Join the sorted lines with a newline character (`\n`).
   - Base64-encode this resulting string.
   - Save the base64-encoded output to exactly `/home/user/release_diff.b64`.

2. **Create the Python Backend (Validation & Decoding)**
   Write and run a Python HTTP server script at `/home/user/server.py` using ONLY the Python standard library (no third-party packages like Flask/FastAPI).
   - The server must listen on `127.0.0.1:9000`.
   - On any `GET` request, it must check for the presence of the `X-Release-Auth` HTTP header.
   - If the header is exactly `YXBwcm92ZWQ=` (which is base64 for "approved"), the server must read `/home/user/release_diff.b64`, decode the base64 content back to plaintext, and return it with an HTTP 200 status code.
   - If the header is missing or incorrect, it must return an HTTP 403 Forbidden status.
   - Run this server in the background.

3. **Configure Reverse Proxy & Rate Limiting**
   Configure Nginx as a reverse proxy in user-space (since you do not have root access).
   - Create an Nginx configuration file at `/home/user/nginx.conf`.
   - Configure it to run entirely under `/home/user/` or `/tmp/` (e.g., set `pid`, `error_log`, `access_log`, `client_body_temp_path`, etc., to writable paths).
   - Listen on `127.0.0.1:8080`.
   - Proxy all incoming requests to the Python server at `127.0.0.1:9000`.
   - Implement rate limiting: restrict clients to **30 requests per minute** based on their IP address (using standard `limit_req_zone` and `limit_req`). Set burst to 5, and do not delay requests.
   - Start Nginx using: `nginx -c /home/user/nginx.conf`

Ensure both your Python server and Nginx are running in the background when you consider the task complete.