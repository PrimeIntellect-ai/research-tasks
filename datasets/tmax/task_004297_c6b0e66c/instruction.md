You are a DevSecOps engineer enforcing "Policy as Code" for internal services. A development team has deployed a test API server running locally at `https://127.0.0.1:8443`. Your job is to write an automated Python assessment script that acts as a vulnerability scanner and policy verifier for this endpoint.

Write a Python script at `/home/user/enforcer.py` that performs the following actions:

1. **Token Generation:** 
   The endpoint requires authentication. Generate a JSON Web Token (JWT) using the `PyJWT` library.
   - Payload must contain: `{"sub": "policy_scanner", "role": "auditor"}`
   - Secret key to sign: `devsecops_secret_2024`
   - Algorithm: `HS256`

2. **TLS Certificate Inspection:**
   The server is using a self-signed certificate. Your script must programmatically fetch the SSL certificate presented by `127.0.0.1` on port `8443`.
   - Extract the Common Name (CN) of the certificate's Issuer.

3. **Vulnerability & Policy Scanning:**
   Send an HTTPS GET request to `https://127.0.0.1:8443/api/health`.
   - You must include the generated JWT in the `Authorization` header as a Bearer token (`Authorization: Bearer <your_token>`).
   - You will need to disable SSL certificate verification in your HTTP client since the certificate is self-signed.
   - Analyze the HTTP response headers. Corporate policy dictates that every endpoint MUST include the following security headers:
     - `X-Content-Type-Options`
     - `Strict-Transport-Security`
     - `Content-Security-Policy`

4. **Reporting:**
   The script must output its findings by creating a JSON file at `/home/user/report.json` with the exact following structure:
   ```json
   {
     "jwt_generated": "<the_token_string_you_created>",
     "issuer_cn": "<extracted_issuer_common_name>",
     "status_code": <integer_http_status_code_received>,
     "policy_violations": ["list", "of", "the", "required", "headers", "that", "are", "MISSING"]
   }
   ```

You may use `pip` to install `requests` and `PyJWT` if they are not already installed. When you have finished writing and running the script, verify that `/home/user/report.json` exists and contains the correct data.