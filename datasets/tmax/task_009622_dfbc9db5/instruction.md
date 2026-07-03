You are a network engineer tasked with inspecting and auditing an internal API service running on a local server.

Here is the information you have:
1. A local HTTPS API service is running on 127.0.0.1 on a port somewhere between 8000 and 9000.
2. The service uses JWT for authentication. We intercepted a standard user token:
   `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoidXNlciJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c`
3. We suspect the API's JWT validation is vulnerable to the "alg=none" bypass.
4. The endpoint `/admin/data` contains sensitive information but requires a token with the role `admin`.
5. The server uses a custom TLS certificate. The CA certificate needed to verify it is located at `/home/user/ca.crt`.

Your objective:
1. Audit the local services to find the correct port.
2. Craft a malicious JWT token that exploits the "alg=none" vulnerability to elevate your privileges to `role: admin` and `user: admin`.
3. Write a Python script at `/home/user/fetch_data.py` that sends an authenticated GET request to the `https://127.0.0.1:<PORT>/admin/data` endpoint using your crafted token.
   - Your Python script **must** strictly validate the server's TLS certificate using the `/home/user/ca.crt` file (do not disable SSL verification).
4. The successful response will be a JSON object in the format: `{"data": "<secret_string>", "sha256": "<hash>"}`.
5. In your script, compute the SHA-256 hash of the `data` string and verify it matches the `sha256` value provided in the response.
6. If the integrity check passes, write ONLY the `<secret_string>` into a file named `/home/user/secret.txt`.
7. Finally, ensure the file `/home/user/secret.txt` has strictly read-only permissions for the owner, and no permissions for anyone else (i.e., `400` or `-r--------`).

Complete the task by ensuring `/home/user/secret.txt` is created with the correct content and permissions.