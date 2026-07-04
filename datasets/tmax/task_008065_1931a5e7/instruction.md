You are acting as a security auditor tasked with fixing permissions and redacting sensitive data for a vulnerable system. You must write a Go program `/home/user/auditor.go` to perform a set of security mitigation tasks. You are restricted to using only the Go standard library (no third-party packages like `golang-jwt/jwt`).

Your Go program must perform the following three tasks when executed:

1. **Sensitive Data Redaction**: 
   Read the file `/home/user/server_response.json` (which contains an array of log messages). You must find all 16-digit credit card numbers formatted as `XXXX-XXXX-XXXX-XXXX` and redact them so that the first 12 digits are replaced with asterisks, leaving only the last 4 digits visible (e.g., `****-****-****-1234`). Save the modified JSON object to `/home/user/redacted.json`. Maintain the original JSON structure.

2. **Token Generation**:
   You need to generate a valid JSON Web Token (JWT) to authenticate your audit requests. Construct an HMAC-SHA256 signed JWT with the secret key `auditor-secret-2023`. 
   - The JWT Header must exactly be: `{"alg":"HS256","typ":"JWT"}`
   - The JWT Payload must exactly be: `{"role":"auditor"}`
   - Use standard Base64URL encoding (without padding) for the parts.
   Write the final token string to `/home/user/auditor_token.txt`.

3. **Content Security Policy Enforcement**:
   To secure the web server's responses, generate a file `/home/user/csp.conf` containing exactly the Nginx directive required to enforce a strict Content Security Policy that only allows resources from the same origin. The file must contain exactly:
   `add_header Content-Security-Policy "default-src 'self'";`

Ensure your Go program compiles and runs successfully, producing the required output files. You must create and run the program yourself to generate the files.