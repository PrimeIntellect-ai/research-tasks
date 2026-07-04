You are a penetration tester tasked with analyzing and patching a vulnerable multi-service application written in Go. The application consists of two services located in `/app/`:
1. **Auth Service**: Issues authentication tokens.
2. **API Gateway**: Validates tokens, routes requests, and serves content.

Currently, the Auth Service uses a custom, easily reversible XOR cipher (with a static single-byte key of `0x42`) combined with base64 encoding to generate tokens. The payload before encryption is a simple query string, e.g., `role=user`.

Your tasks are as follows:

1. **Vulnerability Exploitation (Cryptanalysis & Payload Encoding):**
   Analyze the weak encryption. Write a Go program at `/home/user/forge.go` that generates a forged token for `role=admin` using the flawed XOR + base64 scheme. When run via `go run /home/user/forge.go`, it must print only the forged base64-encoded token to standard output.

2. **Service Patching (Secure Coding & CSP):**
   The API Gateway (`/app/gateway/main.go`) currently accepts these weak tokens. You must rewrite the validation logic in the gateway. 
   - Modify the gateway to reject the old XOR tokens.
   - Implement secure token validation using HMAC-SHA256. The new expected token format in the `Authorization` header will be `Bearer <base64_payload>.<hex_encoded_hmac>`. The payload for an admin should be `role=admin` (base64 encoded as `cm9sZT1hZG1pbg==`).
   - Use the static secret key `super_secret_hmac_key_123` for the HMAC validation.
   - Add a Content Security Policy (CSP) header to ALL responses from the gateway: `Content-Security-Policy: default-src 'self'`.

3. **Deployment:**
   - Compile both services if necessary.
   - Start the Auth Service so it listens on `127.0.0.1:8081`.
   - Start your modified API Gateway so it listens on `127.0.0.1:8080`.
   - Ensure both services remain running in the background.

The automated verification suite will test the API Gateway over HTTP to ensure it enforces the new token scheme, rejects the old weak tokens, and properly sets the CSP headers.