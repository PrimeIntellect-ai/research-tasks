You are a security engineer tasked with rotating credentials for a legacy service. The old authentication key is hardcoded in a compiled Python bytecode file, and the credential rotation endpoint requires secure interaction over HTTPS with strict TLS verification.

Your task is to:
1. Disassemble the compiled Python file `/home/user/auth_handler.pyc` to extract the hardcoded legacy API key.
2. Write a Python script to send an HTTP POST request to the local rotation endpoint at `https://127.0.0.1:8443/rotate`.
3. Provide the extracted legacy key in the `Authorization` header as a Bearer token (e.g., `Authorization: Bearer <old_key>`).
4. Send a JSON payload containing the new key: `{"new_key": "secure_new_key_2024"}`.
5. You must verify the server's TLS certificate using the CA certificate located at `/home/user/ca.crt`. Do not ignore SSL errors.
6. The successful response will contain a `Set-Cookie` header with a `session_token`. Inspect the response to extract this cookie value.
7. Inspect the server's TLS certificate to find its Subject Common Name (CN).

Finally, create a text file at `/home/user/rotation_summary.txt` with exactly three lines:
Line 1: The extracted old API key.
Line 2: The exact value of the `session_token` cookie extracted from the HTTP response.
Line 3: The Subject Common Name (CN) of the server's TLS certificate.

Note: The local HTTPS server is already running on port 8443. All necessary files (`auth_handler.pyc`, `ca.crt`) are present in `/home/user/`.