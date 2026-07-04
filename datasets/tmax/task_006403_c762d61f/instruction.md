You are a security engineer tasked with rotating the master credentials for a legacy internal web service. The source code for this service has been lost, but the compiled binary is currently running on the server.

Recent security audits revealed that the proprietary JWT-based authentication mechanism implemented in this service is vulnerable: it incorrectly accepts tokens where the algorithm is set to "none", bypassing signature verification entirely.

Your objective is to exploit this vulnerability to authorize yourself as an administrator, locate the hidden credential rotation endpoint, and trigger a key rotation. 

Here are the details and requirements:
1. The vulnerable service binary is located at `/home/user/legacy_service`. It is already running and listening on `http://127.0.0.1:8080`.
2. Analyze the binary to discover the hidden API endpoint used for credential rotation. The endpoint path contains the word `rotate`.
3. The service expects an `Authorization: Bearer <token>` header. A valid admin payload must contain the JSON claim `{"role": "admin"}`.
4. Forge a JWT that leverages the `alg: none` vulnerability to bypass signature validation. Note that standard JWTs use Base64URL encoding (without padding) for the header, payload, and signature components.
5. Write a complete Go program at `/home/user/exploit.go` that:
   - Constructs the malicious JWT.
   - Sends an HTTP POST request to the discovered rotation endpoint with the forged token.
   - Reads the JSON response from the server.
6. The server will respond with a JSON object containing the new credentials. Save the exact raw JSON response body to `/home/user/rotation_result.json`.

Ensure your Go script handles the HTTP request properly and that the final output file `/home/user/rotation_result.json` contains the successful rotation confirmation.