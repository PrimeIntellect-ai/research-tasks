You are acting as a security auditor for an internal microservices application. The application issues encrypted authorization tokens to users, but we suspect the tokens are vulnerable to manipulation (specifically, bit-flipping attacks on the encrypted payload and weak checksum validation). 

The application consists of three services located in `/app/`:
1. Nginx API Gateway (running on port 8080)
2. Auth Service (Go binary running on port 8081)
3. Resource Service (Go binary running on port 8082)

Your task is to secure this pipeline by doing the following:

Phase 1: Build a Cryptographic Token Classifier (Go)
Write a Go program at `/home/user/validator/main.go`. This program must serve as an HTTP server on port 8083 with a single endpoint `/validate` that accepts a `GET` request. The token will be provided in the `Authorization` header as a Bearer token.
The token format is a base64-encoded string representing an AES-128-CBC encrypted payload. 
The encryption key is `SuperSecretKey12` (16 bytes) and the IV is the first 16 bytes of the decoded token, followed by the ciphertext.
When decrypted, the plaintext is a JSON string containing `{"user":"<name>", "role":"<role>", "checksum":"<md5>"}`.
Legitimate tokens have a valid MD5 checksum of the `user` and `role` concatenated (`user+role`). Malicious actors have been exploiting the lack of MAC in CBC mode to flip bits and elevate their role to `admin`, updating the payload but often failing to correctly update the MD5 checksum or leaving garbled JSON padding.
Your Go validator must:
- Extract the Bearer token, decode it from base64, and decrypt it using AES-128-CBC.
- Parse the resulting JSON payload.
- Reject the request (return HTTP 403) if the JSON is malformed, if the padding is corrupted, or if the `checksum` does not exactly match the MD5 hash of the concatenated `user` and `role` fields.
- Accept the request (return HTTP 200) if all checks pass.
Compile your Go code to an executable file located at `/home/user/validator-bin` and run it in the background.

Phase 2: Reconfigure the Gateway
Modify the Nginx configuration file located at `/app/nginx/nginx.conf`.
Configure it so that all requests to `/resource` (which proxy to the Resource Service on port 8082) first pass through an `auth_request` to your new validator service running on `http://127.0.0.1:8083/validate`.
Restart or reload Nginx to apply these changes.

Phase 3: Verification Logs
Once your validator is running and Nginx is configured, we will test your setup. Ensure your Go service writes a log file to `/home/user/audit.log` recording each token it processes, with the format: `[TOKEN] - [ACCEPT/REJECT]`.