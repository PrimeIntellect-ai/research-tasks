You are a security engineer responsible for rotating credentials and sanitizing legacy logs for a backend microservice. The service is being updated to use a new mutual TLS (mTLS) certificate and a new set of JWT access tokens. 

Your task consists of three parts: Certificate Validation, Token Generation, and Sensitive Data Redaction.

**Part 1: Certificate Chain Validation**
You have been provided with a directory of new candidate certificates in `/home/user/certs/`. 
The directory contains:
- `ca.crt`: The root Certificate Authority.
- `intermediate.crt`: The intermediate CA.
- `candidate_1.crt`, `candidate_2.crt`, `candidate_3.crt`: Three potential leaf certificates.

Only ONE of the candidate certificates has a valid trust chain back to `ca.crt` through `intermediate.crt`. 
Identify the valid leaf certificate. Extract its Common Name (CN) from its Subject field. This CN is the new symmetric secret for the next part.

**Part 2: Token Generation**
Using the CN extracted in Part 1 as the HMAC-SHA256 secret key, generate a new HS256 JSON Web Token (JWT).
The token must have the following exact payload:
`{"service": "backend", "role": "admin", "exp": 1893456000}`
The header must be:
`{"alg": "HS256", "typ": "JWT"}`
Write the final generated JWT string to a file at `/home/user/new_token.txt`.

**Part 3: Sensitive Data Redaction**
The application logs at `/home/user/app/service.log` contain leaked credentials from the previous deployment.
You must read this log file and redact sensitive information based on the following rules:
1. The old secret was `SUPER_SECRET_LEGACY_V1`. Replace all occurrences of this exact string with `[REDACTED_SECRET]`.
2. Replace all occurrences of any JWT-like strings in the logs with `[REDACTED_TOKEN]`. A JWT-like string in this context is defined as any string matching the regex pattern: `eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+`
Save the sanitized log to `/home/user/app/service_redacted.log`.

**Constraints & Notes:**
- You may use Python and standard Linux utilities (OpenSSL, grep, sed, etc.). You can install Python packages (e.g., `pyjwt`, `cryptography`) if needed.
- Ensure the redacted log matches the original line-by-line, with only the specified strings replaced.